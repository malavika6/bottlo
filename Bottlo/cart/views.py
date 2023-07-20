from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, Cartitem, Wishlist
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib import messages
from django.urls import reverse


def cart(request):
    total = 0
    quantity = 0
    cart_items = None
    tax = 0
    grand_total = 0

    try:
        if request.user.is_authenticated:
            cart_items = Cartitem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'store/cart.html', context)


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    # Retrieve the 'action' parameter from the query string
    action = request.GET.get('action')

    current_user = request.user
    product = Product.objects.get(id=product_id)

    if current_user.is_authenticated:
        is_cart_item_exists = Cartitem.objects.filter(
            product=product, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = Cartitem.objects.get(
                product=product, user=current_user)
            if action == 'increment':
                cart_item.quantity += 1
            elif action == 'decrement' and cart_item.quantity > 1:
                cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item = Cartitem.objects.create(
                product=product, quantity=1, user=current_user)

        return redirect('cart')
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))

        is_cart_item_exists = Cartitem.objects.filter(
            product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = Cartitem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = Cartitem.objects.create(
                product=product, quantity=1, cart=cart)

        return redirect('cart')


def remove_cart(request, product_id):
    # Retrieve the 'action' parameter from the query string
    print('helloooooo')
    action = request.GET.get('action')

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = Cartitem.objects.get(
                product=product, user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = Cartitem.objects.get(product=product, cart=cart)
        if action == 'decrement' and cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')



def del_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = Cartitem.objects.get(product=product, user=request.user)
    else:
        cart1 = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = Cartitem.objects.get(product=product, cart=cart1)
    cart_item.delete()
    return redirect('cart')



def apply_coupon(request):
    return render(request,'')


@login_required(login_url='login')
def checkout(request):
    total = 0
    quantity = 0
    cart_items = None
    tax = 0
    grand_total = 0

    try:
        if request.user.is_authenticated:
            cart_items = Cartitem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'store/checkout.html', context)

@login_required(login_url='login')
def wishlist(request):

    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'store/wishlist.html', context)

@login_required(login_url='login')
def add_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    created = Wishlist.objects.get_or_create(product=product, user=request.user)
    if created:
        messages.success(request, 'Product added successfully')
    else:
        messages.info(request, 'Product already in wishlist.')

    redirect_url = request.META.get('HTTP_REFERER')
    if not redirect_url:
        # Fallback URL if HTTP Referer header is not available
        redirect_url = reverse('wishlist')

    redirect_url += f'?product_id={product_id}'

    return redirect(redirect_url)

@login_required(login_url='login')
def del_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(product=product, user=request.user).delete()
    messages.success(request, 'product removed successfully')
    return redirect('wishlist')
