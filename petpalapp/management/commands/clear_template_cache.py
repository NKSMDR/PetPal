from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.template import engines
import os
import shutil

class Command(BaseCommand):
    help = 'Clears template cache and __pycache__ directories'

    def handle(self, *args, **options):
        # Clear cache
        cache.clear()
        self.stdout.write(self.style.SUCCESS('✓ Cache cleared'))
        
        # Clear template engine cache
        for engine in engines.all():
            if hasattr(engine, 'engine'):
                engine.engine.template_loaders = []
        self.stdout.write(self.style.SUCCESS('✓ Template engine cache cleared'))
        
        # Remove __pycache__ directories
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        count = 0
        for root, dirs, files in os.walk(base_dir):
            if '__pycache__' in dirs:
                pycache_path = os.path.join(root, '__pycache__')
                try:
                    shutil.rmtree(pycache_path)
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Could not remove {pycache_path}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'✓ Removed {count} __pycache__ directories'))
        self.stdout.write(self.style.SUCCESS('\n✓ All caches cleared! Now restart your server with: python manage.py runserver'))
