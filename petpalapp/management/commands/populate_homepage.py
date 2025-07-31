# management/commands/populate_homepage.py
from django.core.management.base import BaseCommand
from petpalapp.models import (
    HeroSection, ParallaxSection, CategoryCard, Testimonial, 
    DogBreed, CareTip, NewsletterSection, HowItWorksStep
)


class Command(BaseCommand):
    help = 'Populate homepage with initial data'

    def handle(self, *args, **options):
        # Create Hero Section
        hero, created = HeroSection.objects.get_or_create(
            defaults={
                'title': 'Find Your Perfect Canine Companion 🐕🦴',
                'subtitle': 'Buy. Sell. Love. Everything your dog needs in one place!',
                'browse_button_text': 'Browse Dogs',
                'sell_button_text': 'Sell Dogs',
                'browse_button_url': '#',
                'sell_button_url': '#',
                'is_active': True
            }
        )

        # Create Parallax Section
        parallax, created = ParallaxSection.objects.get_or_create(
            defaults={
                'title': 'Adopt. Train. Love. 🐾',
                'subtitle': 'Every dog deserves a loving home. Your perfect furry friend is waiting!',
                'button_text': 'Explore Available Dogs',
                'button_url': '#',
                'is_active': True
            }
        )

        # Create Category Cards
        categories = [
            {
                'title': 'Puppies',
                'description': 'Adorable puppies ready to join your family.',
                'button_text': 'View Puppies',
                'button_url': '#',
                'order': 1
            },
            {
                'title': 'Adult Dogs',
                'description': 'Well-trained adult dogs looking for forever homes.',
                'button_text': 'View Adult Dogs',
                'button_url': '#',
                'order': 2
            },
            {
                'title': 'Dog Accessories',
                'description': 'Premium dog food, toys, leashes, and grooming supplies.',
                'button_text': 'Shop Now',
                'button_url': '/dog-accessories',
                'order': 3
            }
        ]

        for category_data in categories:
            CategoryCard.objects.get_or_create(
                title=category_data['title'],
                defaults=category_data
            )

        # Create Testimonials
        testimonials = [
            {
                'content': 'Found my German Shepherd here – best decision ever!',
                'author_name': 'Rajesh Kumar',
                'rating': 5,
                'order': 1
            },
            {
                'content': 'Amazing selection of dog accessories and premium food.',
                'author_name': 'Priya Sharma',
                'rating': 5,
                'order': 2
            },
            {
                'content': 'Sold my Golden Retriever puppies quickly. Great platform!',
                'author_name': 'Amit Patel',
                'rating': 5,
                'order': 3
            }
        ]

        for testimonial_data in testimonials:
            Testimonial.objects.get_or_create(
                author_name=testimonial_data['author_name'],
                defaults=testimonial_data
            )

        # Create Dog Breeds
        breeds = [
            {'name': 'Labrador Retriever', 'popularity_rank': 1, 'is_featured': True},
            {'name': 'Golden Retriever', 'popularity_rank': 2, 'is_featured': True},
            {'name': 'German Shepherd', 'popularity_rank': 3, 'is_featured': True},
            {'name': 'Siberian Husky', 'popularity_rank': 4, 'is_featured': True},
            {'name': 'French Bulldog', 'popularity_rank': 5, 'is_featured': True},
            {'name': 'Beagle', 'popularity_rank': 6, 'is_featured': True},
            {'name': 'Poodle', 'popularity_rank': 7, 'is_featured': True},
            {'name': 'Rottweiler', 'popularity_rank': 8, 'is_featured': True},
        ]

        for breed_data in breeds:
            DogBreed.objects.get_or_create(
                name=breed_data['name'],
                defaults=breed_data
            )

        # Create Care Tips
        care_tips = [
            {
                'title': 'Health & Wellness',
                'description': 'Regular vet checkups, vaccinations, and preventive care for a healthy pup.',
                'category': 'health',
                'icon_class': 'fas fa-heart',
                'order': 1
            },
            {
                'title': 'Training & Behavior',
                'description': 'Positive reinforcement training tips for obedience and socialization.',
                'category': 'training',
                'icon_class': 'fas fa-graduation-cap',
                'order': 2
            },
            {
                'title': 'Nutrition & Diet',
                'description': 'Premium dog food recommendations and feeding guidelines by breed and age.',
                'category': 'nutrition',
                'icon_class': 'fas fa-utensils',
                'order': 3
            }
        ]

        for tip_data in care_tips:
            CareTip.objects.get_or_create(
                title=tip_data['title'],
                defaults=tip_data
            )

        # Create How It Works Steps
        steps = [
            {
                'step_number': 1,
                'title': 'Browse or Post a Dog',
                'description': 'Check available dogs or log in to post your furry friend!',
                'order': 1
            },
            {
                'step_number': 2,
                'title': 'Get Matched',
                'description': 'Connect with buyers/sellers and ask about temperament, health, and training.',
                'order': 2
            },
            {
                'step_number': 3,
                'title': 'Welcome Your New Best Friend',
                'description': 'Complete adoption and bring home your loyal canine companion!',
                'order': 3
            }
        ]

        for step_data in steps:
            HowItWorksStep.objects.get_or_create(
                step_number=step_data['step_number'],
                defaults=step_data
            )

        # Create Newsletter Section
        newsletter, created = NewsletterSection.objects.get_or_create(
            defaults={
                'title': 'Subscribe For Dog Care Tips & Offers',
                'subtitle': 'Get weekly tips on dog training, health, and exclusive deals on dog accessories!',
                'button_text': 'Subscribe',
                'placeholder_text': 'Enter your email',
                'is_active': True
            }
        )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated homepage data!')
        )