from django.shortcuts import get_object_or_404
from products.models import Product
from decimal import Decimal
from django.conf import settings


def cart_contents(request):
    """
    Ensures that the cart contents are available when rendering every page
    """
    
    cart = request.session.get('cart', {})
    
    cart_items = []
    total = 0
    product_count = 0
    for item_id, item_data in cart.items():
        # If we're working w/ an item with no sizes, item_data will be the quantity
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            cart_items.append({'item_id':item_id, 'quantity': item_data, 'product': product})
        # Otherwise we need to add items for each size
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                cart_items.append({'item_id':item_id, 'quantity': quantity, 'product': product, 'size': size})

    # Calculate shipping cost if order is < settings.FREE_SHIPPING_THRESHOLD:
    if total <= settings.FREE_SHIPPING_THRESHOLD:
        shipping = total * Decimal(settings.STANDARD_SHIPPING_PERCENTAGE/100)
        free_shipping_delta = settings.FREE_SHIPPING_THRESHOLD - total
    else:
        shipping = 0
        free_shipping_delta = 0

    grand_total = shipping + total
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'shipping': shipping,
        'free_shipping_delta': free_shipping_delta,
        'free_shipping_threshold': settings.FREE_SHIPPING_THRESHOLD,
        'grand_total': grand_total,
    }
    
    return context