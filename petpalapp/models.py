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


class Pet(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('sold', 'Sold/Adopted'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='pets')
    age = models.CharField(max_length=20, help_text="e.g., '2 months', '1 year', '3 years'")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price in USD")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets_for_sale')
    description = models.TextField(help_text="Detailed description of the pet")
    
    # Images
    image = models.ImageField(upload_to='pets/', help_text="Main pet photo")
    image2 = models.ImageField(upload_to='pets/', blank=True, null=True, help_text="Additional photo")
    image3 = models.ImageField(upload_to='pets/', blank=True, null=True, help_text="Additional photo")
    
    # Pet details
    weight = models.CharField(max_length=20, blank=True, help_text="e.g., '5 kg', '15 lbs'")
    color = models.CharField(max_length=50, blank=True, help_text="Pet's color/markings")
    vaccination_status = models.BooleanField(default=False, help_text="Is the pet vaccinated?")
    health_certificate = models.BooleanField(default=False, help_text="Has health certificate?")
    
    # Location
    city = models.CharField(max_length=100, help_text="City where pet is located")
    state = models.CharField(max_length=50, help_text="State/Province")
    
    # Status and features
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_featured = models.BooleanField(default=False, help_text="Show in featured section")
    is_urgent = models.BooleanField(default=False, help_text="Urgent adoption/sale")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.breed.name}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.breed.name}"
    
    @property
    def is_available(self):
        return self.status == 'available'
    
    @property
    def main_image(self):
        return self.image.url if self.image else None