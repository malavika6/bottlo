from django.shortcuts import render, redirect
from store.models import product
from .models import Cart, Cartitem
from django.http import HttpResponse 



def cart(request):

    return render(request, 'store/cart.html')
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    Product = product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    try:
        cart_item = Cartitem.objects.get(product=Product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except Cartitem.DoesNotExist:
        cart_item = Cartitem.objects.create(
            product=Product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()

    return HttpResponse(cart_item.product)
    exit()
   
    return redirect('cart')

