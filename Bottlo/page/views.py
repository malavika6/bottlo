from django.shortcuts import render
from store.models import Product
from category.models import category


def home(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        "product": products,}
    return render(request, 'home.html', context)

def custom_404(request, exception):
    return render(request, '404.html', status=404)

