def cart_quantity(request):
    """Контекстный процессор для передачи количества товаров в корзине."""
    cart = request.session.get('cart', {})
    cart_total_quantity = sum(item['quantity'] for item in cart.values())  # Общее количество товаров
    return {'cart_total_quantity': cart_total_quantity}
