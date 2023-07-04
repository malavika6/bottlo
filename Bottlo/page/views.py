from django.shortcuts import render, redirect
from store.models import Product
from category.models import category
from order.models import Order
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def home(request):
    products = Product.objects.filter(
        is_available=True).prefetch_related('productimage_set')
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        "product": paged_products, }
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
    return render(request, "account/profile.html", context)
