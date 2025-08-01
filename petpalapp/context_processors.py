def cart_context(request):
    """
    Context processor to provide cart information to all templates
    """
    cart_count = 0
    
    if request.user.is_authenticated:
        # For logged-in users, get cart from user-specific session key
        user_cart_key = f'cart_user_{request.user.id}'
        cart = request.session.get(user_cart_key, [])
    else:
        # For anonymous users, use temporary session cart
        cart = request.session.get('cart', [])
    
    # Calculate total items in cart
    cart_count = sum(item.get('qty', 1) for item in cart)
    
    return {
        'cart_count': cart_count,
        'has_cart_items': cart_count > 0,
    }
