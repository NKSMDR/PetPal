from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
import uuid

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
    image2 = models.ImageField(upload_to='accessories/', blank=True, null=True)
    image3 = models.ImageField(upload_to='accessories/', blank=True, null=True)
    image4 = models.ImageField(upload_to='accessories/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def is_discounted(self):
        return self.original_price and self.original_price > self.price
    
    def get_all_images(self):
        """Return list of all available images for this accessory"""
        images = []
        if self.image:
            images.append(self.image)
        if self.image2:
            images.append(self.image2)
        if self.image3:
            images.append(self.image3)
        if self.image4:
            images.append(self.image4)
        return images
    
    def __str__(self):
        return self.name


class Pet(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    STATUS_CHOICES = [
        ('pending_review', 'Pending Review'),
        ('available', 'Available'),
        ('pending', 'Pending Sale'),
        ('sold', 'Sold/Adopted'),
        ('rejected', 'Rejected'),
    ]
    
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
    address = models.CharField(max_length=255, blank=True, help_text="Full address from map selection")
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True, help_text="Latitude coordinate")
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True, help_text="Longitude coordinate")
    
    # Status and features
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_review')
    is_featured = models.BooleanField(default=False, help_text="Show in featured section")
    is_urgent = models.BooleanField(default=False, help_text="Urgent adoption/sale")
    is_user_submitted = models.BooleanField(default=False, help_text="Submitted by user (not admin)")
    
    # Admin review fields
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_pets')
    review_date = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, help_text="Admin notes for review")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug using breed name and timestamp to ensure uniqueness
            import uuid
            self.slug = slugify(f"{self.breed.name}-{uuid.uuid4().hex[:8]}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.breed.name} - {self.get_gender_display()} - ${self.price}"
    
    @property
    def is_available(self):
        return self.status == 'available'
    
    @property
    def main_image(self):
        return self.image.url if self.image else None


class Order(models.Model):
    """Order model to track customer orders"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_id = models.CharField(max_length=100, unique=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.order_id} - {self.customer.username}"


class OrderItem(models.Model):
    """Individual items within an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_type = models.CharField(max_length=20)  # 'accessory' or 'pet'
    product_id = models.PositiveIntegerField()
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity}"


class Cart(models.Model):
    """User-specific shopping cart"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def get_total(self):
        """Calculate total cart value"""
        total = sum(item.get_subtotal() for item in self.items.all())
        return total
    
    def get_item_count(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Individual items in a user's cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_type = models.CharField(max_length=20)  # 'accessory' or 'pet'
    product_id = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cart', 'product_type', 'product_id')
    
    def __str__(self):
        return f"{self.product_type} {self.product_id} x{self.quantity}"
    
    def get_product(self):
        """Get the actual product object"""
        if self.product_type == 'accessory':
            return Accessory.objects.get(id=self.product_id)
        return None
    
    def get_subtotal(self):
        """Calculate subtotal for this cart item"""
        product = self.get_product()
        if product:
            return product.price * self.quantity
        return 0


class Transaction(models.Model):
    """Transaction model for eSewa payments"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    transaction_uuid = models.CharField(max_length=100, unique=True)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    transaction_date = models.DateTimeField(auto_now_add=True)
    esewa_response = models.JSONField(blank=True, null=True)  # Store eSewa response data
    
    def __str__(self):
        return f"Transaction {self.transaction_uuid} - {self.transaction_status}"