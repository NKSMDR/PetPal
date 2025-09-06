from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib import messages

# Register your models here.
from django.contrib import admin
from .models import Breed, Accessory, Pet, UserProfile

# Create proxy models for separate admin sections
class BrowsePet(Pet):
    class Meta:
        proxy = True
        verbose_name = "Browse Pet (Admin Added)"
        verbose_name_plural = "Browse Pets (Admin Added)"

class MarketplacePet(Pet):
    class Meta:
        proxy = True
        verbose_name = "Marketplace Pet (User Submitted)"
        verbose_name_plural = "Marketplace Pets (User Submitted)"

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
    list_display = ['name', 'category', 'price_display', 'discount_badge', 'image_preview', 'view_actions']
    search_fields = ['name', 'description', 'category']
    list_filter = ['category', 'price']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview', 'discount_info']
    
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price', 'discount_info')
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
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
                '<span style="color: #e74c3c; font-weight: bold;">${}</span> '
                '<span style="text-decoration: line-through; color: #7f8c8d;">${}</span>',
                obj.price, obj.original_price
            )
        return f"${obj.price}"
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
                '<div style="color: #27ae60; font-weight: bold;">Discount: ${} ({}% off)</div>',
                discount_amount, discount_percent
            )
        return "No discount applied"
    discount_info.short_description = "Discount Information"
    
    def view_actions(self, obj):
        return format_html('<a href="#" class="button">Edit</a>')
    view_actions.short_description = "Actions"

admin.site.register(Accessory, AccessoryAdmin)


# Separate admin for Browse Pets (Admin-added pets only)
class BrowsePetAdmin(admin.ModelAdmin):
    list_display = ['breed', 'age', 'gender', 'price', 'status', 'is_featured', 'city', 'image_preview', 'view_detail']
    list_filter = ['breed', 'gender', 'status', 'is_featured', 'is_urgent', 'vaccination_status', 'city', 'created_at']
    search_fields = ['breed__name', 'description', 'city', 'seller__username', 'seller__first_name', 'seller__last_name']
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
        ('Location', {
            'fields': ('city', 'state')
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


# Separate admin for Marketplace Review (User-submitted pets only)
class MarketplacePetAdmin(admin.ModelAdmin):
    list_display = ['breed', 'age', 'gender', 'price', 'status_badge', 'seller_info', 'city', 'submission_date', 'image_preview', 'review_actions']
    list_filter = ['breed', 'gender', 'status', 'vaccination_status', 'city', 'created_at']
    search_fields = ['breed__name', 'description', 'city', 'seller__username', 'seller__first_name', 'seller__last_name']
    readonly_fields = ['image_preview', 'created_at', 'updated_at', 'seller', 'is_user_submitted', 'slug']
    actions = ['approve_selected_pets', 'reject_selected_pets']
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_user_submitted=True)
    
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
    
    def review_actions(self, obj):
        if obj.status == 'pending_review':
            return format_html(
                '<span style="color: #ffc107; font-weight: bold;">⏳ Pending Review</span>'
            )
        elif obj.status == 'available':
            return format_html('<a href="/marketplace/pet/{}" target="_blank" class="button">View on Site</a>', obj.pk)
        elif obj.status == 'rejected':
            return format_html('<span style="color: #dc3545; font-weight: bold;">❌ Rejected</span>')
        return "-"
    review_actions.short_description = "Actions"
    
    def approve_selected_pets(self, request, queryset):
        updated = queryset.filter(status='pending_review').update(
            status='available',
            reviewed_by=request.user,
            review_date=timezone.now()
        )
        self.message_user(request, f'{updated} pets approved successfully.')
    approve_selected_pets.short_description = "Approve selected pets"
    
    def reject_selected_pets(self, request, queryset):
        updated = queryset.filter(status='pending_review').update(
            status='rejected',
            reviewed_by=request.user,
            review_date=timezone.now()
        )
        self.message_user(request, f'{updated} pets rejected.')
    reject_selected_pets.short_description = "Reject selected pets"

admin.site.register(MarketplacePet, MarketplacePetAdmin)

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

# Customize admin site headers
admin.site.site_header = "PetPal Administration"
admin.site.site_title = "PetPal Admin"
admin.site.index_title = "Welcome to PetPal Administration"