from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Breed

class BreedAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'life_span', 'good_with_kids']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Breed, BreedAdmin)


from .models import Accessory

class AccessoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'original_price']
    search_fields = ['name', 'category']
    list_filter = ['category']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Accessory, AccessoryAdmin)