from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from category.models import category
from order.models import Order, OrderProduct
from account.models import AddressBook
from account.forms import AddressForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    products = Product.objects.filter(
        is_available=True).prefetch_related('productimage_set')
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        "product": paged_products, }
    return render(request, 'home.html', context)


def about_us(request):
    return render(request, "includes/about_us.html")


def contact_us(request):
    return render(request, "includes/contact_us.html")


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    addresses = AddressBook.objects.filter(user=request.user).order_by('-id')

    context = {
        'orders': orders,
        'user': user,
        'addresses': addresses

    }
    return render(request, "account/profile.html", context)


def order_detail(request, order_id):
    try:
        ordr_products = OrderProduct.objects.filter(
            order__order_number=order_id)
        order = Order.objects.get(order_number=order_id)

        subtotal = 0
        for i in ordr_products:
            subtotal += i.product_price*i.quantity
        tax = (2 * subtotal) / 100
        grand_total = subtotal + tax
        context = {
            'ordr_products': ordr_products,
            'tax': tax,
            'order': order,
            'subtotal': subtotal,
            'grand_total': grand_total
        }
    except Order.DoesNotExist:
        # Handle the case when the order does not exist
        context = {
            'error_message': 'Order does not exist.'
        }

    return render(request, 'account/order_detail.html', context)


def cancel_order(request, order_id):
    print(order_id,'hii')
    try:
        order = Order.objects.get(order_number=order_id)
        print(order_id)
        if order.status == 'Cancelled':
            messages.warning(request, "This order has already been cancelled.")
        else:
            order.status = 'Cancelled'
            order.save()
            messages.success(request, "Order successfully cancelled.")
        return redirect('order_detail', order_id=order_id)

    except ObjectDoesNotExist:
        messages.error(request, "Order does not exist.")
        return redirect('order_detail')


def add_address(request):
    form = AddressForm()

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            print("hhhhh")
            address = form.save(commit=False)
            address.user = request.user
            print(address)
            address.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

    return JsonResponse({'success': False})
