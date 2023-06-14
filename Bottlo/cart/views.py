from django.shortcuts import render,redirect
from store.models import product

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()


def add_cart(request, product_id):
    product = product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cart_item = Cartitem.objects.get(product=product,cart=cart)
        cart_item.quantity+=1
        cart_item.save()
    except Cartitem.DoesNotExist:
        cart_item =Cartitem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    return redirect('cart')


def cart(request):

    return render(request, 'store/cart.html')
