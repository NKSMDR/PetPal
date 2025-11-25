from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Min, Max
from django.db import IntegrityError
from decimal import Decimal, InvalidOperation
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
import json
import uuid
from .models import Breed, Accessory, UserProfile, Pet, Order, OrderItem, Transaction, Cart, CartItem, ListingPayment, ListingPrice
from .forms import PetSubmissionForm
from django_esewa import EsewaPayment

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
    response = redirect('home')
    # Set a flag to clear cart on next page load
    response.set_cookie('clear_cart', 'true', max_age=5)
    return response

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

    # Handle search query
    search_query = request.GET.get('search', '').strip()
    if search_query:
        breeds = breeds.filter(name__icontains=search_query)

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
        'search_query': search_query,
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

def accessory_detail(request, slug):
    accessory = get_object_or_404(Accessory, slug=slug)
    
    # Get related accessories from the same category
    related_accessories = Accessory.objects.filter(
        category=accessory.category
    ).exclude(id=accessory.id)[:4]
    
    context = {
        'accessory': accessory,
        'related_accessories': related_accessories,
    }
    return render(request, 'pages/accessory_detail.html', context)

def accessories(request):
    from django.core.paginator import Paginator
    
    all_accessories = Accessory.objects.all()
    categories = all_accessories.values_list('category', flat=True).distinct()
    min_price_db = all_accessories.aggregate(Min('price'))['price__min'] or 0
    max_price_db = all_accessories.aggregate(Max('price'))['price__max'] or 1000

    accessories = all_accessories

    search_query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip()
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')

    # Apply search filter
    if search_query:
        accessories = accessories.filter(name__icontains=search_query)
    
    # Apply category filter
    if category_filter:
        accessories = accessories.filter(category__iexact=category_filter)

    # Apply price filters with better logic
    try:
        if price_min and price_min not in ['', 'null', 'undefined']:
            price_min_val = Decimal(str(price_min))
            accessories = accessories.filter(price__gte=price_min_val)
        else:
            price_min = min_price_db
    except (InvalidOperation, ValueError, TypeError):
        price_min = min_price_db

    try:
        if price_max and price_max not in ['', 'null', 'undefined']:
            price_max_val = Decimal(str(price_max))
            accessories = accessories.filter(price__lte=price_max_val)
        else:
            price_max = max_price_db
    except (InvalidOperation, ValueError, TypeError):
        price_max = max_price_db

    # Pagination - 8 products per page (2 rows x 4 columns)
    paginator = Paginator(accessories, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/accessories.html', {
        'accessories': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'price_min': price_min,
        'price_max': price_max,
        'min_price_db': min_price_db,
        'max_price_db': max_price_db,
        'page_obj': page_obj,
        'paginator': paginator,
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

def get_or_create_cart(request):
    """Get or create cart for authenticated user"""
    if not request.user.is_authenticated:
        return None
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    return cart

@login_required
def add_to_cart(request, product_type, product_id):
    # Only allow 'accessory' type
    if product_type != 'accessory':
        messages.error(request, 'Invalid product type')
        return redirect('cart')
    
    accessory = get_object_or_404(Accessory, pk=product_id)
    cart = get_or_create_cart(request)
    
    # Try to get existing cart item or create new one
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_type=product_type,
        product_id=product_id,
        defaults={'quantity': 1}
    )
    
    if not created:
        # Item already exists, increment quantity
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{accessory.name} added to cart!')
    return redirect('cart')

@login_required
def remove_from_cart(request, product_type, product_id):
    if product_type != 'accessory':
        return redirect('cart')
    
    cart = get_or_create_cart(request)
    
    try:
        cart_item = CartItem.objects.get(
            cart=cart,
            product_type=product_type,
            product_id=product_id
        )
        cart_item.delete()
        messages.success(request, 'Item removed from cart')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in cart')
    
    return redirect('cart')

@login_required
def update_cart(request, product_type, product_id):
    if request.method == 'POST' and product_type == 'accessory':
        quantity = int(request.POST.get('quantity', 1))
        cart = get_or_create_cart(request)
        
        try:
            cart_item = CartItem.objects.get(
                cart=cart,
                product_type=product_type,
                product_id=product_id
            )
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
        except CartItem.DoesNotExist:
            messages.error(request, 'Item not found in cart')
    
    return redirect('cart')

@login_required
def cart(request):
    cart_items = []
    total = 0
    
    # Get user's database cart
    cart = get_or_create_cart(request)
    
    if cart:
        for cart_item in cart.items.all():
            product = cart_item.get_product()
            if product:
                subtotal = cart_item.get_subtotal()
                cart_items.append({
                    'product': product,
                    'qty': cart_item.quantity,
                    'subtotal': subtotal,
                    'type': cart_item.product_type,
                })
                total += subtotal
    
    return render(request, 'includes/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required
@require_http_methods(["POST"])
def sync_cart(request):
    """Sync cart from frontend localStorage to Django backend"""
    try:
        data = json.loads(request.body)
        cart_data = data.get('cart', [])
        
        if not isinstance(cart_data, list):
            return JsonResponse({'status': 'error', 'message': 'Invalid cart data'}, status=400)
        
        user_cart = get_or_create_cart(request)
        
        # Build frontend cart dictionary
        frontend_items = {}
        for item in cart_data:
            if not all(key in item for key in ['product_type', 'product_id', 'qty']):
                continue
            
            product_type = item['product_type']
            product_id = int(item['product_id'])
            quantity = int(item['qty'])
            
            if quantity < 1 or quantity > 99:
                continue
            
            item_key = (product_type, product_id)
            frontend_items[item_key] = quantity
        
        # Get existing cart items
        existing_items = {
            (cart_item.product_type, cart_item.product_id): cart_item
            for cart_item in user_cart.items.all()
        }
        
        # Update or create items
        for item_key, quantity in frontend_items.items():
            product_type, product_id = item_key
            
            if item_key in existing_items:
                cart_item = existing_items[item_key]
                if cart_item.quantity != quantity:
                    cart_item.quantity = quantity
                    cart_item.save()
            else:
                CartItem.objects.create(
                    cart=user_cart,
                    product_type=product_type,
                    product_id=product_id,
                    quantity=quantity
                )
        
        # Remove items not in frontend cart
        for item_key, cart_item in existing_items.items():
            if item_key not in frontend_items:
                cart_item.delete()
        
        return JsonResponse({'status': 'success', 'message': 'Cart synced'})
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"Error syncing cart: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Sync failed'}, status=500)

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

def sell_pet_info(request):
    """Display sell pet information page with pricing and details"""
    # Get current listing price from database
    listing_price = ListingPrice.get_current_price()
    
    # Check if user has a valid payment with remaining submissions
    has_valid_payment = False
    remaining_submissions = 0
    if request.user.is_authenticated:
        valid_payment = ListingPayment.objects.filter(
            user=request.user,
            status='SUCCESS'
        ).order_by('-payment_date').first()
        
        if valid_payment and valid_payment.has_remaining_submissions():
            has_valid_payment = True
            remaining_submissions = valid_payment.get_remaining_submissions()
    
    context = {
        'listing_price': listing_price,
        'has_valid_payment': has_valid_payment,
        'remaining_submissions': remaining_submissions,
    }
    return render(request, 'pages/sell_pet_info.html', context)

@login_required
def sell_pet_form(request):
    """Handle the actual pet submission form"""
    # Check if user has a payment with remaining submissions
    valid_payment = ListingPayment.objects.filter(
        user=request.user,
        status='SUCCESS'
    ).order_by('-payment_date').first()
    
    if not valid_payment or not valid_payment.has_remaining_submissions():
        messages.error(request, 'You must pay the listing fee before submitting a pet. Please complete the payment first.')
        return redirect('sell_pet')
    
    if request.method == 'POST':
        form = PetSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.seller = request.user  # Ensure seller is the logged-in user
            pet.is_user_submitted = True
            pet.status = 'pending_review'
            pet.save()
            
            # Use one submission from the payment
            valid_payment.use_submission()
            
            remaining = valid_payment.get_remaining_submissions()
            if remaining > 0:
                messages.success(request, f'Your pet has been submitted for review! You have {remaining} submission(s) remaining.')
            else:
                messages.success(request, 'Your pet has been submitted for review! You have used all your submissions.')
            return redirect('my_pets')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PetSubmissionForm()
    
    context = {
        'form': form,
        'payment': valid_payment,
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

def about_us(request):
    """Render the About Us page with company information and store location."""
    return render(request, 'pages/about_us.html')

# eSewa Payment Views
@login_required
@ensure_csrf_cookie  
@login_required
@ensure_csrf_cookie  
def checkout(request):
    """Process checkout for SELECTED items only"""
    print(f"DEBUG Checkout: Method={request.method}, User={request.user}")
    
    # Get user's database cart
    user_cart = get_or_create_cart(request)
    
    if not user_cart or not user_cart.items.exists():
        messages.error(request, 'Your cart is empty! Please add some items to your cart first.')
        return redirect('cart')
    
    # Get selected items from POST data or session
    if request.method == 'POST' and 'selected_items' in request.POST:
        # First time - coming from cart page
        selected_items_json = request.POST.get('selected_items')
        try:
            selected_item_keys = json.loads(selected_items_json)
            request.session['checkout_items'] = selected_item_keys
        except json.JSONDecodeError:
            messages.error(request, 'Invalid selection data.')
            return redirect('cart')
    else:
        # Coming from GET request (showing checkout form)
        selected_item_keys = request.session.get('checkout_items', [])
    
    if not selected_item_keys:
        messages.error(request, 'No items selected for checkout. Please select items from your cart.')
        return redirect('cart')
    
    # Parse selected items (format: "itemId-itemType")
    selected_items = []
    for key in selected_item_keys:
        try:
            item_id, item_type = key.split('-')
            selected_items.append({'id': item_id, 'type': item_type})
        except ValueError:
            continue
    
    if not selected_items:
        messages.error(request, 'Invalid selection. Please try again.')
        return redirect('cart')
    
    # Calculate total and prepare ONLY selected cart items with stock validation
    total = 0
    cart_items = []
    stock_errors = []
    
    for cart_item in user_cart.items.all():
        # Check if this item is in selected list
        is_selected = any(
            s['id'] == str(cart_item.product_id) and s['type'] == cart_item.product_type 
            for s in selected_items
        )
        
        if not is_selected:
            continue  # Skip non-selected items
        
        product = cart_item.get_product()
        if product:
            # Validate stock availability
            if cart_item.product_type == 'accessory':
                if product.stock < cart_item.quantity:
                    stock_errors.append(
                        f"{product.name} - Only {product.stock} available, you have {cart_item.quantity} in cart"
                    )
                    # Update cart to available quantity
                    if product.stock > 0:
                        cart_item.quantity = product.stock
                        cart_item.save()
                    else:
                        cart_item.delete()
                    continue
                elif product.stock == 0:
                    stock_errors.append(f"{product.name} is out of stock")
                    cart_item.delete()
                    continue
            
            subtotal = cart_item.get_subtotal()
            cart_items.append({
                'product': product,
                'qty': cart_item.quantity,
                'subtotal': subtotal,
                'cart_item': cart_item,  # Store reference for later deletion
            })
            total += subtotal
    
    # If there were stock errors, redirect back to cart
    if stock_errors:
        for error in stock_errors:
            messages.error(request, error)
        messages.warning(request, 'Some selected items are no longer available. Please review your cart.')
        return redirect('cart')
    
    # Check if any items remain after validation
    if not cart_items:
        messages.error(request, 'No valid items selected for checkout!')
        return redirect('cart')
    
    print(f"DEBUG Checkout: Total={total}, Selected Items={len(cart_items)}")
    
    if request.method == 'POST':
        print(f"DEBUG Checkout: Processing POST request")
        
        # Create order
        order = Order.objects.create(
            customer=request.user,
            total_amount=total,
            shipping_address=request.POST.get('shipping_address', ''),
            phone=request.POST.get('phone', ''),
            notes=request.POST.get('notes', '')
        )
        
        # Create order items (only for selected items)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_type='accessory',
                product_id=item['product'].id,
                product_name=item['product'].name,
                quantity=item['qty'],
                unit_price=item['product'].price,
                total_price=item['subtotal']
            )
        
        # Store selected cart item IDs for deletion after payment
        selected_cart_item_ids = [item['cart_item'].id for item in cart_items]
        request.session['purchased_cart_items'] = selected_cart_item_ids
        
        # Create transaction
        transaction_uuid = str(uuid.uuid4())
        transaction = Transaction.objects.create(
            order=order,
            transaction_uuid=transaction_uuid,
            transaction_amount=total,
            transaction_status='PENDING'
        )
        
        # Initialize eSewa payment
        epayment = EsewaPayment(
            product_code="EPAYTEST",
            success_url=request.build_absolute_uri(f'/payment/success/{transaction.id}/'),
            failure_url=f'http://localhost:8000/payment/failure/{transaction.id}/',
            secret_key='8gBm/:&EnhH.1/q',
            amount=str(total),
            tax_amount='0',
            product_service_charge='0',
            product_delivery_charge='0',
            total_amount=str(total),
            transaction_uuid=transaction_uuid,
        )
        
        epayment.create_signature()
        
        # Generate form HTML
        form_html = epayment.generate_form()
        
        print("DEBUG: eSewa Form HTML generated for selected items")
        
        context = {
            'order': order,
            'transaction': transaction,
            'form': form_html,
        }
        return render(request, 'pages/checkout.html', context)
    
    # Clear checkout items from session after displaying form
    request.session.pop('checkout_items', None)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'pages/checkout_form.html', context)

def payment_success(request, transaction_id):
    """Handle successful payment - decrease stock and remove ONLY purchased items"""
    transaction = get_object_or_404(Transaction, id=transaction_id)
    order = transaction.order
    
    # Initialize eSewa payment for verification
    epayment = EsewaPayment(
        product_code="EPAYTEST",
        success_url=request.build_absolute_uri(f'/payment/success/{transaction.id}/'),
        failure_url=f'http://localhost:8000/payment/failure/{transaction.id}/',
        secret_key='8gBm/:&EnhH.1/q',
        amount=str(transaction.transaction_amount),
        tax_amount='0',
        product_service_charge='0',
        product_delivery_charge='0',
        total_amount=str(transaction.transaction_amount),
        transaction_uuid=transaction.transaction_uuid,
    )
    epayment.create_signature()
    
    # Verify payment
    if epayment.is_completed(True):
        # Check if stock was already decreased (prevent double processing)
        if transaction.transaction_status != 'SUCCESS':
            # Update transaction and order status
            transaction.transaction_status = 'SUCCESS'
            order.status = 'processing'
            transaction.save()
            order.save()
            
            # ✅ DECREASE STOCK FOR EACH PURCHASED ITEM
            stock_errors = []
            purchased_items = []  # Store purchased items for localStorage removal
            
            for order_item in order.items.all():
                if order_item.product_type == 'accessory':
                    try:
                        accessory = Accessory.objects.get(id=order_item.product_id)
                        
                        # Check if sufficient stock is available
                        if accessory.stock >= order_item.quantity:
                            # Decrease stock
                            accessory.stock -= order_item.quantity
                            accessory.save()
                            print(f"✅ Decreased stock for {accessory.name}: {order_item.quantity} units (New stock: {accessory.stock})")
                            
                            # Add to purchased items list
                            purchased_items.append({
                                'id': str(order_item.product_id),
                                'type': order_item.product_type
                            })
                        else:
                            stock_errors.append(f"{accessory.name} - Only {accessory.stock} available, ordered {order_item.quantity}")
                            print(f"⚠️ Insufficient stock for {accessory.name}")
                    
                    except Accessory.DoesNotExist:
                        stock_errors.append(f"Product ID {order_item.product_id} not found")
                        print(f"❌ Accessory {order_item.product_id} not found")
            
            # ✅ REMOVE ONLY PURCHASED ITEMS FROM DATABASE CART
            user_cart = get_or_create_cart(request)
            purchased_cart_item_ids = request.session.get('purchased_cart_items', [])
            
            if user_cart and purchased_cart_item_ids:
                # Delete only the cart items that were purchased
                deleted_count = user_cart.items.filter(id__in=purchased_cart_item_ids).delete()
                print(f"✅ Removed {deleted_count[0]} purchased items from database cart")
                
                # Clear session
                request.session.pop('purchased_cart_items', None)
            
            # Show warning if there were stock errors
            if stock_errors:
                messages.warning(request, f"Payment successful, but some items had stock issues: {', '.join(stock_errors)}")
        else:
            # Payment already processed, still get purchased items for display
            purchased_items = []
            for order_item in order.items.all():
                purchased_items.append({
                    'id': str(order_item.product_id),
                    'type': order_item.product_type
                })
            print(f"⚠️ Payment already processed for transaction {transaction_id}")
        
        # Pass purchased items to template for localStorage cleanup
        context = {
            'order': order,
            'transaction': transaction,
            'purchased_items': json.dumps(purchased_items),  # Convert to JSON string for template
        }
        
        # Render the correct template path
        return render(request, 'pages/payment_success.html', context)
    else:
        return redirect('payment_failure', transaction_id=transaction.id)


def payment_failure(request, transaction_id):
    """Handle failed payment - DO NOT decrease stock"""
    transaction = get_object_or_404(Transaction, id=transaction_id)
    order = transaction.order
    
    # Update status to failed
    transaction.transaction_status = 'FAILURE'
    order.status = 'cancelled'
    transaction.save()
    order.save()
    
    # ❌ DO NOT decrease stock on failed payment
    print(f"❌ Payment failed for transaction {transaction_id} - Stock NOT decreased")
    
    # Show error message to user
    messages.error(request, 'Payment failed. Your cart items are still saved. Please try again.')
    
    # Context for failure page
    context = {
        'order': order,
        'transaction': transaction,
        'error_message': 'Payment was unsuccessful. Please try again or contact support if the issue persists.',
    }
    
    # ✅ Render a user-friendly HTML page (NOT JSON)
    return render(request, 'pages/payment_failure.html', context)


# Listing Payment Views
@login_required
@ensure_csrf_cookie
def listing_payment_checkout(request):
    """Process listing fee payment"""
    if request.method == 'POST':
        # Get current listing price from database
        listing_price = ListingPrice.get_current_price()
        
        # Create listing payment transaction
        transaction_uuid = str(uuid.uuid4())
        listing_payment = ListingPayment.objects.create(
            user=request.user,
            transaction_uuid=transaction_uuid,
            amount=listing_price,
            status='PENDING'
        )
        
        # Initialize eSewa payment
        epayment = EsewaPayment(
            product_code="EPAYTEST",
            success_url=request.build_absolute_uri(f'/listing-payment/success/{listing_payment.id}/'),
            # success_url=f'http://localhost:8000/listing-payment/success/{listing_payment.id}/',
            failure_url=f'http://localhost:8000/listing-payment/failure/{listing_payment.id}/',
            secret_key='8gBm/:&EnhH.1/q',
            amount=str(listing_price),
            tax_amount='0',
            product_service_charge='0',
            product_delivery_charge='0',
            total_amount=str(listing_price),
            transaction_uuid=transaction_uuid,
        )
        
        epayment.create_signature()
        
        # Generate form HTML
        form_html = epayment.generate_form()
        
        context = {
            'listing_payment': listing_payment,
            'form': form_html,
        }
        return render(request, 'pages/listing_payment_checkout.html', context)
    
    return redirect('sell_pet')


def listing_payment_success(request, payment_id):
    """Handle successful listing payment"""
    listing_payment = get_object_or_404(ListingPayment, id=payment_id)
    
    # Initialize eSewa payment for verification
    epayment = EsewaPayment(
        product_code="EPAYTEST",
        success_url=request.build_absolute_uri(f'/listing-payment/success/{listing_payment.id}/'),
        # success_url=f'http://localhost:8000/listing-payment/success/{listing_payment.id}/',
        failure_url=f'http://localhost:8000/listing-payment/failure/{listing_payment.id}/',
        secret_key='8gBm/:&EnhH.1/q',
        amount=str(listing_payment.amount),
        tax_amount='0',
        product_service_charge='0',
        product_delivery_charge='0',
        total_amount=str(listing_payment.amount),
        transaction_uuid=listing_payment.transaction_uuid,
    )
    epayment.create_signature()
    
    # Verify payment
    if epayment.is_completed(True):
        listing_payment.status = 'SUCCESS'
        listing_payment.save()
        
        messages.success(request, 'Payment successful! You can now submit your pet listing.')
        
        context = {
            'listing_payment': listing_payment,
        }
        return render(request, 'pages/listing_payment_success.html', context)
    else:
        return redirect('listing_payment_failure', payment_id=listing_payment.id)


def listing_payment_failure(request, payment_id):
    """Handle failed listing payment"""
    listing_payment = get_object_or_404(ListingPayment, id=payment_id)
    
    listing_payment.status = 'FAILURE'
    listing_payment.save()
    
    messages.error(request, 'Payment failed. Please try again.')
    
    context = {
        'listing_payment': listing_payment,
    }
    return render(request, 'pages/listing_payment_failure.html', context)

@login_required
def get_product_stock(request, product_type, product_id):
    """Get current stock for a product"""
    try:
        if product_type == 'accessory':
            accessory = get_object_or_404(Accessory, pk=product_id)
            return JsonResponse({
                'status': 'success',
                'stock': accessory.stock,
                'product_name': accessory.name
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid product type'
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)