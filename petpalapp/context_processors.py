def cart_context(request):
    """
    Context processor to provide cart information to all templates
    """
    cart_count = 0
    
    # For now, use session cart for all users
    cart = request.session.get('cart', [])
    cart_count = sum(item.get('qty', 1) for item in cart)
    
    return {
        'cart_count': cart_count,
        'has_cart_items': cart_count > 0,
    }
