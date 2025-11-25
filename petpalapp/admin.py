from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib import messages

# Register your models here.
from django.contrib import admin
from .models import (Breed, Accessory, Pet, UserProfile, Order, OrderItem, Transaction, Cart, CartItem, 
                     ListingPayment, ListingPrice, HeroSection, FeatureCard, Testimonial, HomePageSettings)

# Create proxy models for separate admin sections
class BrowsePet(Pet):
    class Meta:
        proxy = True
        verbose_name = "Professional Pet Listing"
        verbose_name_plural = "Professional Pet Listings"

class MarketplacePet(Pet):
    class Meta:
        proxy = True
        verbose_name = "User Submitted Pet"
        verbose_name_plural = "User Marketplace Pets"

class PendingPet(Pet):
    class Meta:
        proxy = True
        verbose_name = "Pending Review"
        verbose_name_plural = "├─ Pending Review"

class ApprovedPet(Pet):
    class Meta:
        proxy = True
        verbose_name = "Approved Pet"
        verbose_name_plural = "├─ Approved Pets"

class RejectedPet(Pet):
    class Meta:
        proxy = True
        verbose_name = "Rejected Pet"
        verbose_name_plural = "└─ Rejected Pets"

class BreedAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'life_span', 'good_with_kids', 'energy_level', 'image_preview', 'view_detail']
    list_filter = ['size', 'good_with_kids', 'energy_level', 'ease_of_training', 'grooming_requirement']
    search_fields = ['name', 'overview']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'image', 'image_preview', 'overview')
        }),
        ('Physical Characteristics', {
            'fields': ('size', 'weight', 'height', 'life_span')
        }),
        ('Behavioral Traits', {
            'fields': ('energy_level', 'ease_of_training', 'grooming_requirement', 'vocality', 'affection_needs', 'exercise_requirement')
        }),
        ('Family Compatibility', {
            'fields': ('good_with_kids',)
        }),
        ('Care Requirements', {
            'fields': ('exercise', 'grooming')
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 8px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"
    
    def view_detail(self, obj):
        url = reverse('breed_detail', args=[obj.slug])
        return format_html('<a href="{}" target="_blank" class="button">View on Site</a>', url)
    view_detail.short_description = "Actions"

admin.site.register(Breed, BreedAdmin)


class AccessoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_display', 'stock', 'discount_badge', 'image_preview', 'view_actions']
    search_fields = ['name', 'description', 'category']
    list_filter = ['category', 'price', 'stock']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview', 'discount_info', 'stock_status']
    list_editable = []
    
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price', 'discount_info')
        }),
        ('Inventory', {
            'fields': ('stock', 'stock_status')
        }),
        ('Media', {
            'fields': ('image', 'image2', 'image3', 'image4', 'image_preview')
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Preview"
    
    def price_display(self, obj):
        if obj.is_discounted():
            return format_html(
                '<span style="color: #e74c3c; font-weight: bold;">NRS {}</span> '
                '<span style="text-decoration: line-through; color: #7f8c8d;">NRS {}</span>',
                obj.price, obj.original_price
            )
        return f"NRS {obj.price}"
    price_display.short_description = "Price"
    
    def discount_badge(self, obj):
        if obj.is_discounted():
            discount_percent = int(((obj.original_price - obj.price) / obj.original_price) * 100)
            return format_html(
                '<span style="background: #e74c3c; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}% OFF</span>',
                discount_percent
            )
        return ""
    discount_badge.short_description = "Discount"
    
    def discount_info(self, obj):
        if obj.is_discounted():
            discount_amount = obj.original_price - obj.price
            discount_percent = int(((obj.original_price - obj.price) / obj.original_price) * 100)
            return format_html(
                '<div style="color: #27ae60; font-weight: bold;">Discount: NRS {} ({}% off)</div>',
                discount_amount, discount_percent
            )
        return "No discount applied"
    discount_info.short_description = "Discount Information"
    
    def stock_status(self, obj):
        """Display stock status with color coding"""
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            '#dc3545' if obj.stock == 0 else '#ffc107' if obj.stock <= 5 else '#28a745',
            obj.get_stock_status()
        )
    stock_status.short_description = "Stock Status"
    
    def view_actions(self, obj):
        return format_html('<a href="#" class="button">Edit</a>')
    view_actions.short_description = "Actions"

admin.site.register(Accessory, AccessoryAdmin)

# Separate admin for Browse Pets (Admin-added pets only)
class BrowsePetAdmin(admin.ModelAdmin):
    list_display = ['breed', 'age', 'gender', 'price', 'status', 'is_featured', 'image_preview', 'view_detail']
    list_filter = ['breed', 'gender', 'status', 'is_featured', 'is_urgent', 'vaccination_status', 'created_at']
    search_fields = ['breed__name', 'description', 'seller__username', 'seller__first_name', 'seller__last_name']
    prepopulated_fields = {'slug': ('breed',)}
    readonly_fields = ['image_preview', 'created_at', 'updated_at', 'is_user_submitted']
    list_editable = ['is_featured', 'status']
    
    def get_queryset(self, request):
        
        return super().get_queryset(request).filter(is_user_submitted=False)
    
    def has_add_permission(self, request):
        return True  # Admins can add pets
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('slug', 'breed', 'age', 'gender', 'price', 'seller', 'description')
        }),
        ('Pet Details', {
            'fields': ('weight', 'color', 'vaccination_status', 'health_certificate')
        }),
        ('Media', {
            'fields': ('image', 'image2', 'image3', 'image_preview')
        }),
        ('Status & Features', {
            'fields': ('status', 'is_featured', 'is_urgent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 8px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"
    
    def view_detail(self, obj):
        return format_html('<a href="/pets/{}" target="_blank" class="button">View on Site</a>', obj.pk)
    view_detail.short_description = "Actions"

    def save_model(self, request, obj, form, change):
        # Ensure admin-added pets are marked correctly
        obj.is_user_submitted = False
        if not change:  # New pet
            obj.status = 'available'  # Admin pets are available by default
        super().save_model(request, obj, form, change)

admin.site.register(BrowsePet, BrowsePetAdmin)


# Base admin class for marketplace pets
class BaseMarketplacePetAdmin(admin.ModelAdmin):
    list_display = ['breed', 'age', 'gender', 'price', 'status_badge', 'seller_info', 'city', 'submission_date', 'image_preview', 'quick_actions']
    list_filter = ['breed', 'gender', 'vaccination_status', 'city', 'created_at']
    search_fields = ['breed__name', 'description', 'city', 'seller__username', 'seller__first_name', 'seller__last_name']
    readonly_fields = ['image_preview', 'created_at', 'updated_at', 'seller', 'is_user_submitted', 'slug']
    list_per_page = 25
    
    def has_add_permission(self, request):
        return False  # Users add pets via frontend, not admin
    
    fieldsets = (
        ('Pet Information', {
            'fields': ('slug', 'breed', 'age', 'gender', 'price', 'description')
        }),
        ('Seller Information', {
            'fields': ('seller',)
        }),
        ('Pet Details', {
            'fields': ('weight', 'color', 'vaccination_status', 'health_certificate')
        }),
        ('Location', {
            'fields': ('city', 'state')
        }),
        ('Media', {
            'fields': ('image', 'image2', 'image3', 'image_preview')
        }),
        ('Review Status', {
            'fields': ('status', 'reviewed_by', 'review_date', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def status_badge(self, obj):
        colors = {
            'pending_review': '#ffc107',
            'available': '#28a745',
            'pending': '#17a2b8',
            'sold': '#6f42c1',
            'rejected': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"
    
    def seller_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small>{}</small>',
            obj.seller.get_full_name() or obj.seller.username,
            obj.seller.email
        )
    seller_info.short_description = "Seller"
    
    def submission_date(self, obj):
        return obj.created_at.strftime("%b %d, %Y")
    submission_date.short_description = "Submitted"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 8px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"
    
    def quick_actions(self, obj):
        if obj.status == 'pending_review':
            return format_html(
                '<span style="color: #ffc107; font-weight: bold;">⏳ Awaiting Review</span>'
            )
        elif obj.status == 'available':
            return format_html('<a href="/marketplace/pet/{}" target="_blank" class="button">View on Site</a>', obj.pk)
        elif obj.status == 'rejected':
            return format_html('<span style="color: #dc3545; font-weight: bold;">❌ Rejected</span>')
        return "-"
    quick_actions.short_description = "Actions"
    
    def approve_selected_pets(self, request, queryset):
        updated = queryset.update(
            status='available',
            reviewed_by=request.user,
            review_date=timezone.now()
        )
        self.message_user(request, f'{updated} pets approved successfully.', messages.SUCCESS)
    approve_selected_pets.short_description = "✅ Approve selected pets"
    
    def reject_selected_pets(self, request, queryset):
        updated = queryset.update(
            status='rejected',
            reviewed_by=request.user,
            review_date=timezone.now()
        )
        self.message_user(request, f'{updated} pets rejected.', messages.WARNING)
    reject_selected_pets.short_description = "❌ Reject selected pets"


# Admin for Pending Review Pets
class PendingPetAdmin(BaseMarketplacePetAdmin):
    actions = ['approve_selected_pets', 'reject_selected_pets']
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_user_submitted=True, status='pending_review')


# Admin for Approved Pets
class ApprovedPetAdmin(BaseMarketplacePetAdmin):
    actions = ['reject_selected_pets']
    list_display = ['breed', 'age', 'gender', 'price', 'seller_info', 'city', 'submission_date', 'image_preview', 'quick_actions']
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_user_submitted=True, status='available')


# Admin for Rejected Pets
class RejectedPetAdmin(BaseMarketplacePetAdmin):
    actions = ['approve_selected_pets']
    list_display = ['breed', 'age', 'gender', 'price', 'seller_info', 'city', 'submission_date', 'image_preview', 'rejection_info']
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_user_submitted=True, status='rejected')
    
    def rejection_info(self, obj):
        if obj.admin_notes:
            return format_html(
                '<span style="color: #dc3545;">📝 {}</span>',
                obj.admin_notes[:50] + '...' if len(obj.admin_notes) > 50 else obj.admin_notes
            )
        return '-'
    rejection_info.short_description = "Rejection Reason"


# Register all marketplace pet admins
admin.site.register(PendingPet, PendingPetAdmin)
admin.site.register(ApprovedPet, ApprovedPetAdmin)
admin.site.register(RejectedPet, RejectedPetAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone', 'created_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'user_type', 'phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

# Order and Transaction Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'total_amount', 'status', 'created_at', 'view_items']
    list_filter = ['status', 'created_at']
    search_fields = ['order_id', 'customer__username', 'customer__email', 'customer__first_name', 'customer__last_name']
    readonly_fields = ['order_id', 'created_at', 'updated_at']
    list_editable = ['status']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'customer', 'total_amount', 'status')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address', 'phone', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def view_items(self, obj):
        return format_html('<a href="#" class="button">View Items</a>')
    view_items.short_description = "Items"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'product_type', 'quantity', 'unit_price', 'total_price']
    list_filter = ['product_type', 'order__status']
    search_fields = ['product_name', 'order__order_id', 'order__customer__username']
    readonly_fields = ['order', 'product_type', 'product_id', 'product_name', 'quantity', 'unit_price', 'total_price']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_uuid', 'order', 'transaction_amount', 'transaction_status', 'transaction_date']
    list_filter = ['transaction_status', 'transaction_date']
    search_fields = ['transaction_uuid', 'order__order_id', 'order__customer__username']
    readonly_fields = ['transaction_uuid', 'transaction_date', 'esewa_response']
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('order', 'transaction_uuid', 'transaction_amount', 'transaction_status')
        }),
        ('eSewa Response', {
            'fields': ('esewa_response',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('transaction_date',),
            'classes': ('collapse',)
        })
    )

# Cart Admin
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product_type', 'product_id', 'quantity', 'added_at')
    can_delete = True

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_item_count', 'get_total', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CartItemInline]
    
    def get_item_count(self, obj):
        return obj.get_item_count()
    get_item_count.short_description = 'Items'
    
    def get_total(self, obj):
        return f"NRS {obj.get_total():.2f}"
    get_total.short_description = 'Total'


# Listing Payment Admin
@admin.register(ListingPayment)
class ListingPaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_uuid', 'user', 'amount', 'status', 'submission_status', 'payment_date']
    list_filter = ['status', 'payment_date']
    search_fields = ['transaction_uuid', 'user__username', 'user__email']
    readonly_fields = ['transaction_uuid', 'payment_date', 'esewa_response', 'submissions_used']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('user', 'transaction_uuid', 'amount', 'status')
        }),
        ('Submission Tracking', {
            'fields': ('total_submissions_allowed', 'submissions_used'),
            'description': 'Track how many pet submissions have been made with this payment'
        }),
        ('eSewa Response', {
            'fields': ('esewa_response',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('payment_date',),
            'classes': ('collapse',)
        })
    )
    
    def submission_status(self, obj):
        if obj.status != 'SUCCESS':
            return format_html('<span style="color: #6c757d;">N/A</span>')
        
        remaining = obj.get_remaining_submissions()
        if remaining > 0:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">{}/{} used ({} remaining)</span>',
                obj.submissions_used, obj.total_submissions_allowed, remaining
            )
        else:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">{}/{} used (All used)</span>',
                obj.submissions_used, obj.total_submissions_allowed
            )
    submission_status.short_description = "Submission Status"
    
    def has_add_permission(self, request):
        # Prevent manual addition of listing payments
        return False


# Listing Price Admin
@admin.register(ListingPrice)
class ListingPriceAdmin(admin.ModelAdmin):
    list_display = ['price', 'updated_at', 'updated_by']
    readonly_fields = ['updated_at', 'updated_by']
    
    fieldsets = (
        ('Listing Fee Configuration', {
            'fields': ('price',),
            'description': 'Set the listing fee for pet submissions. This price will be shown to users on the sell pet info page.'
        }),
        ('Update Information', {
            'fields': ('updated_at', 'updated_by'),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        # Only allow one listing price configuration
        return not ListingPrice.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of listing price
        return False
    
    def save_model(self, request, obj, form, change):
        # Track who updated the price
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


# Homepage Customization Admin
@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'image_preview', 'updated_at']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'cta_text', 'cta_link')
        }),
        ('Image', {
            'fields': ('background_image', 'image_preview')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def image_preview(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" style="max-width: 300px; max-height: 150px; border-radius: 8px;" />', obj.background_image.url)
        return "No Image"
    image_preview.short_description = "Preview"


@admin.register(FeatureCard)
class FeatureCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'is_active', 'order', 'has_link']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['image_preview']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description', 'link')
        }),
        ('Visual', {
            'fields': ('icon', 'image', 'image_preview'),
            'description': 'Use either an icon OR an image'
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px; border-radius: 8px;" />', obj.image.url)
        return "Using icon instead"
    image_preview.short_description = "Image Preview"
    
    def has_link(self, obj):
        return "✓" if obj.link else "✗"
    has_link.short_description = "Has Link"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating_stars', 'location', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'rating', 'created_at']
    search_fields = ['customer_name', 'testimonial_text', 'location']
    readonly_fields = ['image_preview']
    
    fieldsets = (
        ('Customer Info', {
            'fields': ('customer_name', 'location', 'customer_image', 'image_preview')
        }),
        ('Testimonial', {
            'fields': ('rating', 'testimonial_text')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        })
    )
    
    def image_preview(self, obj):
        if obj.customer_image:
            return format_html('<img src="{}" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover;" />', obj.customer_image.url)
        return "No Image"
    image_preview.short_description = "Photo"
    
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return format_html('<span style="font-size: 18px;">{}</span>', stars)
    rating_stars.short_description = "Rating"


@admin.register(HomePageSettings)
class HomePageSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'tagline', 'show_featured_pets', 'show_testimonials', 'show_features', 'updated_at']
    readonly_fields = ['updated_at', 'image_preview']
    
    fieldsets = (
        ('Site Branding', {
            'fields': ('site_name', 'tagline')
        }),
        ('About Section', {
            'fields': ('about_section_title', 'about_section_text', 'about_image', 'image_preview')
        }),
        ('Section Visibility', {
            'fields': ('show_featured_pets', 'show_testimonials', 'show_features'),
            'description': 'Toggle which sections appear on the homepage'
        }),
        ('Last Updated', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        })
    )
    
    def image_preview(self, obj):
        if obj.about_image:
            return format_html('<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 8px;" />', obj.about_image.url)
        return "No Image"
    image_preview.short_description = "About Image Preview"
    
    def has_add_permission(self, request):
        # Only allow one homepage settings instance
        return not HomePageSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of homepage settings
        return False


# Customize admin site headers
admin.site.site_header = "PetPal Administration"
admin.site.site_title = "PetPal Admin"
admin.site.index_title = "Welcome to PetPal Administration"