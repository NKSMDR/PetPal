# PetPal Homepage Customization System

## Overview
A complete homepage customization system that allows admins to manage all homepage content including hero sections, features, testimonials, and images through the Django admin panel.

## New Models Added

### 1. **HeroSection**
Customizable hero/banner sections with:
- Title and subtitle text
- Background image upload
- Call-to-action button (text + link)
- Active/inactive toggle
- Display order
- **Admin can add multiple hero sections for carousel/rotation**

### 2. **FeatureCard**
Feature cards displayed on homepage:
- Title and description
- Font Awesome icon OR custom image
- Optional link
- Active/inactive toggle
- Display order
- **Perfect for highlighting key features like "Verified Sellers", "Safe Payments", etc.**

### 3. **Testimonial**
Customer testimonials:
- Customer name and photo
- Rating (1-5 stars)
- Testimonial text
- Location
- Active/inactive toggle
- Display order
- **Build trust with customer reviews**

### 4. **HomePageSettings**
General homepage configuration:
- Site name and tagline
- About section (title, text, image)
- Toggle visibility of sections (featured pets, testimonials, features)
- **Single instance - controls overall homepage behavior**

## Admin Interface Features

### Hero Section Admin
- ✅ Image preview in list view
- ✅ Drag-and-drop ordering
- ✅ Quick enable/disable
- ✅ Organized fieldsets
- ✅ Responsive image preview

### Feature Card Admin
- ✅ Icon or image selection
- ✅ Link management
- ✅ Order management
- ✅ Quick enable/disable
- ✅ Visual indicators

### Testimonial Admin
- ✅ Star rating display (⭐⭐⭐⭐⭐)
- ✅ Customer photo preview (circular)
- ✅ Location tracking
- ✅ Order management
- ✅ Quick enable/disable

### Homepage Settings Admin
- ✅ Single instance (can't add multiple)
- ✅ Can't be deleted
- ✅ Section visibility toggles
- ✅ About section management
- ✅ Image preview

## How to Use

### Step 1: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Access Admin Panel
Navigate to: `http://localhost:8000/admin/`

You'll see new sections under "🐾 PetPal Management":
- Hero Sections
- Feature Cards
- Testimonials
- Homepage Settings

### Step 3: Configure Homepage Settings
1. Click on "Homepage Settings"
2. Set your site name and tagline
3. Configure the about section
4. Upload an about image
5. Toggle which sections to show
6. Save

### Step 4: Add Hero Sections
1. Click "Hero Sections" → "Add Hero Section"
2. Enter title (e.g., "Find Your Perfect Companion")
3. Enter subtitle
4. Upload background image (recommended: 1920x800px)
5. Set CTA button text and link
6. Set order (0 = first)
7. Check "Is active"
8. Save

**Tip**: Add multiple hero sections for a carousel effect!

### Step 5: Add Feature Cards
1. Click "Feature Cards" → "Add Feature Card"
2. Enter title (e.g., "Verified Sellers")
3. Enter description
4. Choose icon (e.g., "fas fa-shield-alt") OR upload image
5. Optionally add a link
6. Set order
7. Check "Is active"
8. Save

**Suggested Features**:
- 🛡️ Verified Sellers
- 💳 Secure Payments
- 🏥 Health Certified Pets
- 📞 24/7 Support

### Step 6: Add Testimonials
1. Click "Testimonials" → "Add Testimonial"
2. Enter customer name
3. Upload customer photo (optional)
4. Set rating (1-5)
5. Enter testimonial text
6. Add location
7. Set order
8. Check "Is active"
9. Save

## Image Recommendations

### Hero Background Images
- **Size**: 1920x800px (or similar 16:9 aspect ratio)
- **Format**: JPG or PNG
- **Content**: High-quality pet photos, happy families with pets
- **File Size**: < 500KB (optimize for web)

### Feature Card Images
- **Size**: 400x400px (square)
- **Format**: PNG with transparency preferred
- **Content**: Icons or simple illustrations
- **File Size**: < 100KB

### Testimonial Photos
- **Size**: 200x200px (square)
- **Format**: JPG or PNG
- **Content**: Customer headshots
- **File Size**: < 50KB

### About Section Image
- **Size**: 800x600px (4:3 aspect ratio)
- **Format**: JPG or PNG
- **Content**: Team photo, office, happy pets
- **File Size**: < 300KB

## Font Awesome Icons

Common icons you can use for Feature Cards:

```
fas fa-paw          - Paw print
fas fa-shield-alt   - Shield (security)
fas fa-heart        - Heart (love/care)
fas fa-check-circle - Check mark
fas fa-star         - Star (quality)
fas fa-users        - Community
fas fa-phone        - Support
fas fa-truck        - Delivery
fas fa-certificate  - Certification
fas fa-home         - Home
```

Full icon list: https://fontawesome.com/icons

## Admin Panel Organization

The homepage customization models appear in the sidebar as:

```
🐾 PETPAL MANAGEMENT
├─ ...
├─ Hero Sections 🖼️
├─ Feature Cards ⭐
├─ Testimonials 💬
├─ Homepage Settings ⚙️
└─ ...
```

## Features

### ✅ Implemented
- Full CRUD operations for all homepage elements
- Image upload and preview
- Order management with drag-and-drop
- Active/inactive toggles
- Responsive admin interface
- Image previews in admin
- Star rating display
- Single instance homepage settings
- Organized fieldsets
- Search and filter functionality

### 🎨 Design Benefits
- **Flexible**: Add/remove sections as needed
- **Visual**: See image previews before publishing
- **Organized**: Logical grouping of fields
- **Safe**: Can't delete critical settings
- **User-Friendly**: Clear labels and help text
- **Professional**: Clean admin interface

## Next Steps

### 1. Create Homepage View
Update your `views.py` to fetch and display homepage data:

```python
from .models import HeroSection, FeatureCard, Testimonial, HomePageSettings

def home(request):
    settings = HomePageSettings.get_settings()
    hero_sections = HeroSection.objects.filter(is_active=True)
    features = FeatureCard.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)
    featured_pets = Pet.objects.filter(is_featured=True, status='available')[:6]
    
    context = {
        'settings': settings,
        'hero_sections': hero_sections,
        'features': features,
        'testimonials': testimonials,
        'featured_pets': featured_pets if settings.show_featured_pets else [],
    }
    return render(request, 'pages/home.html', context)
```

### 2. Update Homepage Template
Create a modern, responsive homepage template using the data.

### 3. Add Sample Data
Create initial hero sections, features, and testimonials through the admin panel.

## Troubleshooting

### Images not showing?
- Check `MEDIA_URL` and `MEDIA_ROOT` in settings.py
- Ensure media files are being served in development
- Verify image file permissions

### Can't add homepage settings?
- Only one instance allowed
- If exists, edit the existing one
- Can't be deleted for safety

### Order not working?
- Lower numbers appear first
- Use 0, 10, 20, 30... for easy reordering
- Save after changing order

## Best Practices

1. **Optimize Images**: Compress images before uploading
2. **Use Alt Text**: Add descriptive titles for accessibility
3. **Test Mobile**: Check how images look on mobile devices
4. **Consistent Style**: Use similar image styles across sections
5. **Regular Updates**: Keep testimonials and features fresh
6. **Backup**: Export data before major changes

## Security

- ✅ Only admin users can access customization
- ✅ Image uploads are validated
- ✅ XSS protection on text fields
- ✅ CSRF protection on forms
- ✅ Proper file permissions

---

**Ready to customize your homepage!** 🎨✨

Access admin at: `http://localhost:8000/admin/`
