from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from products.models import Product

# Create your views here.

def view_cart(request):
    """A view that renders the cart contents page"""
    return render(request, "cart/cart.html")
    
    
def add_to_cart(request, item_id):
    """Add a quantity of the specified product to the cart"""
    
    quantity=int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    product = Product.objects.get(id=item_id)

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}')
    else:
        cart[item_id] = quantity
        messages.success(request, f'Added {product.name} to your cart')

    request.session['cart'] = cart
    return redirect(reverse('products'))
    
    
def adjust_cart(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    product = Product.objects.get(id=item_id)
    
    if quantity > 0:
        cart[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}')
    else:
        cart.pop(item_id)
        messages.success(request, f'Removed {product.name} from your cart')
        
    request.session['cart'] = cart
    return redirect(reverse('view_cart'))

def remove_from_cart(request, item_id):
    """Set the quantity of the give item to 0"""
    try:
        cart = request.session.get('cart', {})
        cart.pop(item_id)
        product = Product.objects.get(id=item_id)

        request.session['cart'] = cart
        messages.success(request, f'Removed {product.name} from your cart')
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
