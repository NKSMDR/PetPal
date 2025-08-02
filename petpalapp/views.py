from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Min, Max
from decimal import Decimal, InvalidOperation
from django.utils import timezone
from .models import Breed, Accessory, UserProfile, Pet
from .forms import PetSubmissionForm

def Home(request):
    return render(request, 'pages/home.html')

def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        # Validate input
        if not email or not password:
            messages.error(request, 'Please enter both email and password')
            return render(request, 'pages/login.html')
        
        try:
            # Find user by email
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Your account is deactivated')
            else:
                messages.error(request, 'Invalid email or password')
                
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address')
    
    return render(request, 'pages/login.html')

def Register(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        user_type = request.POST.get('user_type', '')
        
        # Validation
        errors = []
        
        if not all([first_name, last_name, email, phone, password, confirm_password, user_type]):
            errors.append('All fields are required')
        
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long')
            
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        if User.objects.filter(email=email).exists():
            errors.append('An account with this email already exists')
        
        # If there are errors, show them
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'pages/register.html')
        
        try:
            # Create user
            user = User.objects.create_user(
                username=email,  # Use email as username
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Get or create user profile and save additional information
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.phone = phone
            profile.user_type = user_type
            profile.save()
            
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
            
        except IntegrityError:
            messages.error(request, 'An error occurred while creating your account')
    
    return render(request, 'pages/register.html')

def Logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home')

# Your existing views
def breed_detail(request, slug):
    breed = get_object_or_404(Breed, slug=slug)
    return render(request, 'pages/breed_detail.html', {'breed': breed})

def breed_list(request):
    breeds = Breed.objects.all()

    SIZE_CHOICES = ['Small', 'Medium', 'Large']
    LEVEL_CHOICES = ['Low', 'Medium', 'High']
    TRAINING_CHOICES = ['Easy', 'Moderate', 'Difficult']
    GROOMING_CHOICES = ['Low', 'Moderate', 'High']
    VOCALATY_CHOICE = ['Low', 'Moderate', 'High']
    AFFECTION_CHOICE = ['independent', 'balance', 'cuddly']

    filters = {
        "size": request.GET.get("size"),
        "energy_level": request.GET.get("energy_level"),
        "ease_of_training": request.GET.get("ease_of_training"),
        "grooming_requirement": request.GET.get("grooming_requirement"),
        "vocality": request.GET.get("vocality"),
        "affection_needs": request.GET.get("affection_needs"),
        "exercise_requirement": request.GET.get("exercise_requirement"),
    }

    for key, value in filters.items():
        if value:
            breeds = breeds.filter(**{f"{key}__iexact": value})

    kid_friendly = request.GET.get("kid_friendly")
    if kid_friendly == "yes":
        breeds = breeds.filter(good_with_kids=True)
    elif kid_friendly == "no":
        breeds = breeds.filter(good_with_kids=False)

    context = {
        'breeds': breeds,
        'kid_friendly': kid_friendly,
        'size_options': SIZE_CHOICES,
        'level_options': LEVEL_CHOICES,
        'training_options': TRAINING_CHOICES,
        'grooming_options': GROOMING_CHOICES,
        'vocality_options': VOCALATY_CHOICE,
        'affection_options': AFFECTION_CHOICE,
        **filters,
    }

    return render(request, 'pages/breed_list.html', context)

def accessories(request):
    all_accessories = Accessory.objects.all()
    categories = all_accessories.values_list('category', flat=True).distinct()
    min_price_db = all_accessories.aggregate(Min('price'))['price__min'] or 0
    max_price_db = all_accessories.aggregate(Max('price'))['price__max'] or 1000

    accessories = all_accessories

    search_query = request.GET.get('q')
    category_filter = request.GET.get('category')
    price_min = request.GET.get('price_min') or min_price_db
    price_max = request.GET.get('price_max') or max_price_db

    if search_query:
        accessories = accessories.filter(name__icontains=search_query)
    if category_filter:
        accessories = accessories.filter(category__iexact=category_filter)

    try:
        if price_min not in [None, '', 'null']:
            price_min_val = Decimal(int(float(price_min)))
            accessories = accessories.filter(price__gte=price_min_val)
    except (InvalidOperation, ValueError):
        pass

    try:
        if price_max not in [None, '', 'null']:
            price_max_val = Decimal(int(float(price_max)))
            accessories = accessories.filter(price__lte=price_max_val)
    except (InvalidOperation, ValueError):
        pass

    return render(request, 'pages/accessories.html', {
        'accessories': accessories,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'price_min': price_min,
        'price_max': price_max,
        'min_price_db': min_price_db,
        'max_price_db': max_price_db,
    })


@login_required
def profile(request):
    # Get or create user profile to handle missing profile cases
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = UserProfile.objects.create(user=request.user)
    
    context = {
        'user': request.user,
        'profile': profile
    }
    return render(request, 'pages/profile.html', context)

def get_cart(request):
    """Get cart items for both anonymous and authenticated users"""
    return request.session.get('cart', [])

def save_cart(request, cart_data):
    """Save cart for anonymous users (logged-in users save automatically via ORM)"""
    request.session['cart'] = cart_data
    request.session.modified = True

def add_to_cart(request, product_type, product_id):
    # Only allow 'accessory' type
    if product_type != 'accessory':
        return redirect('cart')
    
    accessory = get_object_or_404(Accessory, pk=product_id)
    
    # Session cart for all users for now
    cart = get_cart(request)
    found = False
    for item in cart:
        if item['product_type'] == product_type and item['product_id'] == product_id:
            item['qty'] += 1
            found = True
            break
    if not found:
        cart.append({'product_type': product_type, 'product_id': product_id, 'qty': 1})
    save_cart(request, cart)
    
    return redirect('cart')

def remove_from_cart(request, product_type, product_id):
    if product_type != 'accessory':
        return redirect('cart')
    
    # Session cart for all users for now
    cart = get_cart(request)
    cart[:] = [item for item in cart if not (item['product_type'] == product_type and item['product_id'] == product_id)]
    save_cart(request, cart)
    
    return redirect('cart')

def update_cart(request, product_type, product_id):
    if request.method == 'POST' and product_type == 'accessory':
        quantity = int(request.POST.get('quantity', 1))
        
        # Session cart for all users for now
        cart = get_cart(request)
        for item in cart:
            if item['product_type'] == product_type and item['product_id'] == product_id:
                item['qty'] = quantity
                break
        save_cart(request, cart)
    
    return redirect('cart')

def cart(request):
    cart_items = []
    total = 0
    
    # Session cart for all users for now
    cart = get_cart(request)
    for item in cart:
        if item['product_type'] == 'accessory':
            product = get_object_or_404(Accessory, pk=item['product_id'])
            subtotal = product.price * item['qty']
            cart_items.append({
                'product': product,
                'qty': item['qty'],
                'subtotal': subtotal,
                'type': item['product_type'],
            })
            total += subtotal
    
    return render(request, 'includes/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

def browse_pets(request):
    # Only show admin-added pets (not user-submitted ones)
    pets = Pet.objects.filter(is_user_submitted=False, status='available')
    breed = request.GET.get('breed')
    age = request.GET.get('age')
    size = request.GET.get('size')
    search_query = request.GET.get('q')

    if breed:
        pets = pets.filter(breed__name__iexact=breed)
    if age:
        pets = pets.filter(age__iexact=age)
    if size:
        pets = pets.filter(size__iexact=size)
    if search_query:
        pets = pets.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    context = {
        'pets': pets,
        'breed': breed,
        'age': age,
        'size': size,
        'search_query': search_query,
    }
    return render(request, 'pages/browse_pets.html', context)

def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk, status='available')
    
    # Get related pets (same breed, different pet, available only)
    related_pets = Pet.objects.filter(
        breed=pet.breed, 
        status='available'
    ).exclude(id=pet.id)[:4]
    
    context = {
        'pet': pet,
        'related_pets': related_pets,
    }
    return render(request, 'pages/pet_detail.html', context)

@login_required
def sell_pet(request):
    if request.method == 'POST':
        form = PetSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.seller = request.user  # Ensure seller is the logged-in user
            pet.is_user_submitted = True
            pet.status = 'pending_review'
            pet.save()
            
            messages.success(request, 'Your pet has been submitted for review! Our admin team will review it shortly.')
            return redirect('my_pets')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PetSubmissionForm()
    
    context = {
        'form': form,
    }
    return render(request, 'pages/sell_pet.html', context)

@login_required
def my_pets(request):
    """Display user's submitted pets and their status"""
    user_pets = Pet.objects.filter(seller=request.user, is_user_submitted=True).order_by('-created_at')
    
    context = {
        'user_pets': user_pets,
    }
    return render(request, 'pages/my_pets.html', context)

def marketplace(request):
    """Display approved user-submitted pets only"""
    pets = Pet.objects.filter(
        status='available',
        is_user_submitted=True
    ).order_by('-created_at')
    
    # Filter options
    breed = request.GET.get('breed')
    age = request.GET.get('age')
    city = request.GET.get('city')
    search_query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if breed:
        pets = pets.filter(breed__name__icontains=breed)
    if age:
        pets = pets.filter(age__icontains=age)
    if city:
        pets = pets.filter(city__icontains=city)
    if search_query:
        pets = pets.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(breed__name__icontains=search_query)
        )
    
    # Price filtering
    if min_price:
        try:
            pets = pets.filter(price__gte=Decimal(min_price))
        except (ValueError, InvalidOperation):
            pass
    if max_price:
        try:
            pets = pets.filter(price__lte=Decimal(max_price))
        except (ValueError, InvalidOperation):
            pass

    # Get unique values for filters
    breeds = Breed.objects.all().order_by('name')
    cities = Pet.objects.filter(
        status='available', 
        is_user_submitted=True
    ).values_list('city', flat=True).distinct().order_by('city')

    context = {
        'pets': pets,
        'breeds': breeds,
        'cities': cities,
        'breed': breed,
        'age': age,
        'city': city,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'pages/marketplace.html', context)

def marketplace_pet_detail(request, pk):
    # Only show approved user-submitted pets
    pet = get_object_or_404(Pet, pk=pk, status='available', is_user_submitted=True)
    
    # Get related marketplace pets (same breed, different pet, available and user-submitted only)
    related_pets = Pet.objects.filter(
        breed=pet.breed, 
        status='available',
        is_user_submitted=True
    ).exclude(id=pet.id)[:4]
    
    context = {
        'pet': pet,
        'related_pets': related_pets,
        'is_marketplace': True,  # Flag to differentiate in template
    }
    return render(request, 'pages/marketplace_pet_detail.html', context)