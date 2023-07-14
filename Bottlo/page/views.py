from django.shortcuts import render, redirect
from store.models import Product
from category.models import category
from order.models import Order
from account.models import AddressBook
from account.forms import AddressForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages


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
    orders = Order.objects.filter(user=user).order_by('-created_at')
    addresses = AddressBook.objects.filter(user= request.user).order_by('-id')

    context = {
        'orders': orders,
        'user':user,
        'addresses':addresses
        
    }
    return render(request, "account/profile.html", context)

# def  add_address(request):
#     form = AddressForm()
#     if request.method == "POST":
#         form = AddressForm(request.POST)
#         if form.is_valid():
#             saveform=form.save(commit=False)
#             saveform.user= request.user
#             saveform.save()
#             messages.success(request,"New Address added sucessfully.!")
#             return redirect('my_addresses')
#     context={
#         'form':form
#     }
