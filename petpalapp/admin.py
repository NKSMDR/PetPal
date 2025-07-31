from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

# Register your models here.
from django.contrib import admin
from .models import Breed, Accessory

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

# Customize admin site headers
admin.site.site_header = "PetPal Administration"
admin.site.site_title = "PetPal Admin"
admin.site.index_title = "Welcome to PetPal Administration"