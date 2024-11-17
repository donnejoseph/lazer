from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ProductPage

def add_to_cart(request, product_id):
    """Добавление товара в корзину."""
    try:
        product = ProductPage.objects.get(id=product_id)
    except ProductPage.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Товар не найден'}, status=404)

    cart = request.session.get('cart', {})

    # Получаем первое изображение товара
    first_image = product.images.first()  # Извлекаем первое связанное изображение
    image_url = first_image.image.url if first_image and first_image.image else None

    # Добавляем товар в корзину
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.title,
            'price': str(product.price),
            'quantity': 1,
            'image': image_url
        }

    request.session['cart'] = cart

    # Обновляем общее количество товаров в корзине
    cart_total_quantity = sum(item['quantity'] for item in cart.values())

    return JsonResponse({
        'status': 'success',
        'message': 'Товар добавлен в корзину',
        'cart_total_quantity': cart_total_quantity
    })


def view_cart(request):
    """Просмотр содержимого корзины"""
    cart = request.session.get('cart', {})
    cart_total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    cart_total_quantity = sum(item['quantity'] for item in cart.values())  # Общее количество товаров
    products = ProductPage.objects.all()[0:16]

    return render(request, 'mypages/cart.html', {
        'cart': cart,
        'cart_total': cart_total,
        'cart_total_quantity': cart_total_quantity,  # Передаем общее количество товаров
        'products': products
    })


def remove_from_cart(request, product_id):
    """Удалить товар из корзины"""
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('view_cart')  # Возвращаем на страницу корзины

def update_cart(request, product_id, action):
    """Обновление количества товара в корзине."""
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if action == 'increase':
            cart[str(product_id)]['quantity'] += 1
        elif action == 'decrease' and cart[str(product_id)]['quantity'] > 1:
            cart[str(product_id)]['quantity'] -= 1

        request.session['cart'] = cart

        # Подсчитываем итоговую стоимость и количество товаров
        cart_total_quantity = sum(item['quantity'] for item in cart.values())
        cart_total = sum(float(item['price']) * item['quantity'] for item in cart.values())

        return JsonResponse({
            'success': True,
            'cart_total_quantity': cart_total_quantity,
            'cart_total': cart_total
        })
    else:
        return JsonResponse({'success': False, 'message': 'Товар не найден в корзине'}, status=404)

