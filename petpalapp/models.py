from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('buyer', 'Buy/Adopt Pets'),
        ('seller', 'Sell/List Pets'),
        ('both', 'Both Buy and Sell'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

# Automatically create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()


class Breed(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='breed/')

    # General Info
    life_span = models.CharField(max_length=30, default='10-12 years')
    size = models.CharField(max_length=20, default='Medium')  # Small, Medium, Large
    weight = models.CharField(max_length=20, default='Unknown')
    height = models.CharField(max_length=20, default='Unknown')
    exercise  = models.CharField(max_length=20, default='Unknown')
    grooming= models.CharField(max_length=20,default='unknown')

    overview = models.TextField(default='No overview available at this time.')
    good_with_kids = models.BooleanField(default=True)

    # FILTERABLE TRAITS with defaults 🔥
    energy_level = models.CharField(max_length=50, default='Medium')
    ease_of_training = models.CharField(max_length=50, default='Moderate')
    grooming_requirement = models.CharField(max_length=50, default='Medium')
    vocality = models.CharField(max_length=50, default='Medium')
    affection_needs = models.CharField(max_length=50, default='Moderate')
    exercise_requirement = models.CharField(max_length=50, default='Medium')

    def __str__(self):
        return self.name


class Accessory(models.Model):
    CATEGORY_CHOICES = [
        ('Collar', 'Collar'),
        ('Leash', 'Leash'),
        ('Toy', 'Toy'),
        ('Bowl', 'Bowl'),
        ('Bed', 'Bed'),
        ('Clothes', 'Clothes'),
        ('Food', 'Food'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    original_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='accessories/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def is_discounted(self):
        return self.original_price and self.original_price > self.price
    def __str__(self):
        return self.name