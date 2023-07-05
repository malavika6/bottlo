from cart.views import _cart_id
from . models import Cart,Cartitem,Wishlist

def Counter(request):
    cart_count = 0
    if "admin" in request.path:
        return{}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = Cartitem.objects.all().filter(user=request.user)
            else:
                cart_items = Cartitem.objects.all().filter(cart=cart[:1])
            for item in cart_items:
                cart_count += item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)

def wishlist_counter(request):
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return {'wishlist_count': wishlist_count}