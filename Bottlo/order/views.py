from django.shortcuts import render,redirect
from cart.models import Cartitem

def place_order(request):
    current_user = request.user
    cart_items = Cartitem.objects.filter(user=current_user)
    cart_count =cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    
    
    
