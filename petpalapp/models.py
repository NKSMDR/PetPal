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
    stock = models.PositiveIntegerField(default=0, help_text="Number of items in stock")
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
    
    def is_in_stock(self):
        """Check if item is in stock"""
        return self.stock > 0
    
    def is_out_of_stock(self):
        """Check if item is out of stock"""
        return self.stock == 0
    
    def decrease_stock(self, quantity=1):
        """Decrease stock by specified quantity"""
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
            return True
        return False
    
    def get_stock_status(self):
        """Get stock status as string"""
        if self.stock == 0:
            return "Out of Stock"
        elif self.stock <= 5:
            return f"Low Stock ({self.stock} left)"
        else:
            return f"In Stock ({self.stock} available)"
    
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
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price in NPR (Nepalese Rupees)")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets_for_sale')
    description = models.TextField(help_text="Detailed description of the pet")
    
    # Images
    image = models.ImageField(upload_to='pets/', help_text="Main pet photo")
    image2 = models.ImageField(upload_to='pets/', blank=True, null=True, help_text="Additional photo")
    image3 = models.ImageField(upload_to='pets/', blank=True, null=True, help_text="Additional photo")
    
    # Pet details
    weight = models.CharField(max_length=20, blank=True, help_text="e.g., '5 kg', '15 lbs'")
    color = models.CharField(max_length=50, blank=True, help_text="Pet's color/markings")
    GENDER_AVAILABILITY_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('both', 'Both'),
    ]
    gender_availability = models.CharField(
        max_length=10, 
        choices=GENDER_AVAILABILITY_CHOICES, 
        blank=True, 
        null=True,
        help_text="Gender availability: Male, Female, or Both"
    )
    vaccination_status = models.BooleanField(default=False, help_text="Is the pet vaccinated?")
    health_certificate = models.BooleanField(default=False, help_text="Has health certificate?")
    health_certificate_file = models.FileField(upload_to='health_certificates/', blank=True, null=True, help_text="Upload health certificate (PDF/Image)")
    
    # Location
    city = models.CharField(max_length=100, help_text="City where pet is located")
    state = models.CharField(max_length=50, help_text="State/Province")
    address = models.CharField(max_length=255, blank=True, help_text="Full address from map selection")
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True, help_text="Latitude coordinate")
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True, help_text="Longitude coordinate")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_review')
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


class ListingPrice(models.Model):
    """Admin-configurable listing price"""
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100.00, help_text="Listing fee in NPR")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='listing_price_updates')
    
    class Meta:
        verbose_name = "Listing Price Configuration"
        verbose_name_plural = "Listing Price Configuration"
    
    def __str__(self):
        return f"NPR {self.price}"
    
    @classmethod
    def get_current_price(cls):
        """Get the current listing price, create default if doesn't exist"""
        price_config = cls.objects.first()
        if not price_config:
            price_config = cls.objects.create(price=100.00)
        return price_config.price


class ListingPayment(models.Model):
    """Payment model for pet listing fees - allows 5 pet submissions per payment"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing_payments')
    transaction_uuid = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_date = models.DateTimeField(auto_now_add=True)
    esewa_response = models.JSONField(blank=True, null=True)
    
    # Multi-pet submission tracking
    total_submissions_allowed = models.IntegerField(default=5, help_text="Number of pets that can be submitted with this payment")
    submissions_used = models.IntegerField(default=0, help_text="Number of pet submissions already made")
    
    def __str__(self):
        return f"Listing Payment {self.transaction_uuid} - {self.user.username} - {self.submissions_used}/{self.total_submissions_allowed} used"
    
    def has_remaining_submissions(self):
        """Check if this payment still has available submissions"""
        return self.status == 'SUCCESS' and self.submissions_used < self.total_submissions_allowed
    
    def get_remaining_submissions(self):
        """Get number of remaining submissions"""
        if self.status != 'SUCCESS':
            return 0
        return max(0, self.total_submissions_allowed - self.submissions_used)
    
    def use_submission(self):
        """Increment the submissions used counter"""
        if self.has_remaining_submissions():
            self.submissions_used += 1
            self.save()
            return True
        return False
    
    class Meta:
        ordering = ['-payment_date']


class HeroSection(models.Model):
    """Homepage hero section with customizable images and text"""
    title = models.CharField(max_length=200, default="Find Your Perfect Companion")
    subtitle = models.CharField(max_length=300, default="Discover loving pets and quality accessories")
    background_image = models.ImageField(upload_to='homepage/hero/', help_text="Hero background image (recommended: 1920x800px)")
    cta_text = models.CharField(max_length=50, default="Browse Pets", help_text="Call-to-action button text")
    cta_link = models.CharField(max_length=200, default="/browse-pets/", help_text="Button link URL")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"
    
    def __str__(self):
        return f"{self.title} - {'Active' if self.is_active else 'Inactive'}"


class FeatureCard(models.Model):
    """Feature cards displayed on homepage"""
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    icon = models.CharField(max_length=50, default="fas fa-paw", help_text="Font Awesome icon class (e.g., 'fas fa-paw')")
    image = models.ImageField(upload_to='homepage/features/', blank=True, null=True, help_text="Optional image instead of icon")
    link = models.CharField(max_length=200, blank=True, help_text="Link URL (optional)")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Feature Card"
        verbose_name_plural = "Feature Cards"
    
    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """Customer testimonials for homepage"""
    customer_name = models.CharField(max_length=100)
    customer_image = models.ImageField(upload_to='homepage/testimonials/', blank=True, null=True, help_text="Customer photo (optional)")
    rating = models.IntegerField(default=5, help_text="Rating out of 5")
    testimonial_text = models.TextField(max_length=500)
    location = models.CharField(max_length=100, blank=True, help_text="e.g., 'Kathmandu, Nepal'")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return f"{self.customer_name} - {self.rating}★"


class HomePageSettings(models.Model):
    """General homepage settings"""
    site_name = models.CharField(max_length=100, default="PetPal")
    tagline = models.CharField(max_length=200, default="Your Trusted Pet Marketplace")
    about_section_title = models.CharField(max_length=100, default="About PetPal")
    about_section_text = models.TextField(default="We connect loving families with their perfect pets.")
    about_image = models.ImageField(upload_to='homepage/', blank=True, null=True)
    show_featured_pets = models.BooleanField(default=True, help_text="Show featured pets section")
    show_testimonials = models.BooleanField(default=True, help_text="Show testimonials section")
    show_features = models.BooleanField(default=True, help_text="Show features section")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Homepage Settings"
        verbose_name_plural = "Homepage Settings"
    
    def __str__(self):
        return f"Homepage Settings - {self.site_name}"
    
    @classmethod
    def get_settings(cls):
        """Get or create homepage settings"""
        settings = cls.objects.first()
        if not settings:
            settings = cls.objects.create()
        return settings


class Wishlist(models.Model):
    """Wishlist linked to a single user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"


class WishlistItem(models.Model):
    """Individual pet entries in a wishlist"""
    SOURCE_CHOICES = [
        ('browse_pets', 'Browse Pets'),
        ('marketplace', 'Marketplace'),
    ]
    
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='wishlist_items', null=True, blank=True)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)  # Keep for backward compatibility
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='browse_pets')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']
        unique_together = ('wishlist', 'pet')

    def __str__(self):
        return f"{self.pet.breed.name} (Pet #{self.pet.id}) in {self.wishlist.user.username}'s wishlist"
    
    def save(self, *args, **kwargs):
        # Auto-populate breed from pet if not set
        if not self.breed_id and self.pet:
            self.breed = self.pet.breed
        super().save(*args, **kwargs)


class ChatThread(models.Model):
    """
    Conversation between a buyer and a seller about a specific marketplace pet.
    One thread per (pet, buyer) pair.
    """
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='chat_threads')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_chat_threads')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_chat_threads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('pet', 'buyer')
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat about {self.pet} between {self.buyer} and {self.seller}"


class ChatMessage(models.Model):
    """
    Individual message within a ChatThread.
    """
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender} in {self.thread}"