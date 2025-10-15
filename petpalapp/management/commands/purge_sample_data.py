from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

from petpalapp.models import Pet, Accessory, Breed

import os


class Command(BaseCommand):
    help = "Purge sample/random data from the database with optional media cleanup."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without actually deleting",
        )
        parser.add_argument(
            "--only-user-submitted",
            action="store_true",
            help="Only delete user-submitted items (e.g., Pet.is_user_submitted=True)",
        )
        parser.add_argument(
            "--include-breeds",
            action="store_true",
            help="Also delete Breed entries (use with care)",
        )
        parser.add_argument(
            "--with-media",
            action="store_true",
            help="Delete associated media files on disk for removed objects",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        only_user_submitted = options["only_user_submitted"]
        include_breeds = options["include_breeds"]
        with_media = options["with_media"]

        self.stdout.write(self.style.WARNING("Starting purge of sample data"))
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN enabled - no changes will be made"))

        # Build querysets
        pet_qs = Pet.objects.all()
        if only_user_submitted:
            pet_qs = pet_qs.filter(is_user_submitted=True)

        accessory_qs = Accessory.objects.all()

        breed_qs = Breed.objects.all() if include_breeds else Breed.objects.none()

        total_pets = pet_qs.count()
        total_accessories = accessory_qs.count()
        total_breeds = breed_qs.count()

        self.stdout.write(f"Pets to delete: {total_pets}")
        self.stdout.write(f"Accessories to delete: {total_accessories}")
        if include_breeds:
            self.stdout.write(self.style.NOTICE(f"Breeds to delete: {total_breeds}"))

        # Collect media paths (before deletion)
        def existing_path(field):
            if not field:
                return None
            try:
                if hasattr(field, 'path') and os.path.exists(field.path):
                    return field.path
            except Exception:
                return None
            return None

        pet_media_paths = []
        for pet in pet_qs:
            pet_media_paths.extend(filter(None, [
                existing_path(pet.image),
                existing_path(pet.image2),
                existing_path(pet.image3),
            ]))

        accessory_media_paths = []
        for acc in accessory_qs:
            accessory_media_paths.extend(filter(None, [
                existing_path(acc.image),
                existing_path(acc.image2),
                existing_path(acc.image3),
                existing_path(acc.image4),
            ]))

        if dry_run:
            self.stdout.write(self.style.SUCCESS("Dry run summary:"))
            self.stdout.write(f" - Would delete {total_pets} pets")
            self.stdout.write(f" - Would delete {total_accessories} accessories")
            if include_breeds:
                self.stdout.write(f" - Would delete {total_breeds} breeds")
            if with_media:
                self.stdout.write(f" - Would delete {len(pet_media_paths) + len(accessory_media_paths)} media files")
            return

        with transaction.atomic():
            # Delete DB rows
            deleted_pets = pet_qs.delete()[0]
            deleted_accessories = accessory_qs.delete()[0]
            deleted_breeds = 0
            if include_breeds:
                deleted_breeds = breed_qs.delete()[0]

        self.stdout.write(self.style.SUCCESS(
            f"Deleted: pets={deleted_pets}, accessories={deleted_accessories}, breeds={deleted_breeds}"
        ))

        # Delete media files after DB delete (non-atomic)
        if with_media:
            removed_files = 0
            for path in set(pet_media_paths + accessory_media_paths):
                try:
                    if os.path.exists(path):
                        os.remove(path)
                        removed_files += 1
                except Exception as exc:
                    self.stderr.write(f"Failed to remove {path}: {exc}")
            self.stdout.write(self.style.SUCCESS(f"Removed media files: {removed_files}"))


