from django.shortcuts import render,redirect
from store.models import Product
from category.models import category
from order.models import Order


def home(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        "product": products,}
    return render(request, 'home.html', context)

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def profile(request):
    user = request.user
    print(user)
    orders = Order.objects.filter(user=user).order_by('-created_at')
    
    
    context = {
        'orders': orders,
    }
    return render(request,"account/profile.html", context)



