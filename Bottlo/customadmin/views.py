from django.shortcuts import render, redirect, get_object_or_404
from store.admin import ProductAdmin
from store.models import Product
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ProductEditForm, CategoryForm, CouponForm
from . models import Coupon
from category.models import category
from order.models import Order, OrderProduct, Payment
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from account.models import Account
from PIL import Image
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def supuser(request):

    total_revenue = Payment.objects.aggregate(
        total=Sum('amount_paid')).get('total', 0)
    total_order_count = Order.objects.count()
    product_count = Product.objects.count()
    category_count = category.objects.count()
    orders = Order.objects.all().order_by('-created_at')
    orderpayment = Payment.objects.all()

    context = {
        'orders': orders,
        'orderpayment': orderpayment,
        'total_revenue': total_revenue,
        'total_order_count': total_order_count,
        'product_count': product_count,
        'category_count': category_count
    }
    return render(request, 'supuser/adminhome.html', context)


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='login')
def usermanagement(request):

    users = Account.objects.filter(
        is_superadmin=False).order_by('id').reverse()
    context = {
        'users': users,
    }
    return render(request, 'supuser/usermanagement.html', context)


def block_user(request, id):
    if request.method == 'POST':
        pi = Account.objects.get(id=id)
        pi.is_active = False
        pi.save()
        return redirect('usermanagement')


def unblock_user(request, id):
    if request.method == 'POST':
        pi = Account.objects.get(id=id)
        pi.is_active = True
        pi.save()
        return redirect('usermanagement')
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# @login_required(login_url='login')
# def product_list(request,category_slug=None):
#     categories = None
#     products = None

#     if category_slug is not None:
#         categories = get_object_or_404(category, slug=category_slug)
#         products = Product.objects.filter(category=categories, is_available=True).prefetch_related('productimage_set')
#         paginator = Paginator(products, 6)
#         page = request.GET.get('page')
#         paged_products = paginator.get_page(page)
#         product_count = products.count()

#     else:
#         products = Product.objects.all().filter(is_available=True).prefetch_related('productimage_set')
#         paginator = Paginator(products, 9)
#         page = request.GET.get('page')
#         paged_products = paginator.get_page(page)
#         product_count = products.count()
#         categories = category.objects.all()

#     context = {
#         "product": paged_products,
#         "product_count": product_count,
#         "categories": categories,
#     }

#     return render(request, "supuser/product.html", context)


def product_list(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True).prefetch_related('productimage_set')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(
            is_available=True).prefetch_related('productimage_set')
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        categories = category.objects.all()
    context = {
        "product": paged_products,
        "product_count": product_count,
        "categories": categories,
    }
    return render(request, "supuser/product.html", context)

    # Rest of the code for rendering the product list page without a specific category


def search(request):
    keyword = request.GET.get('keyword')
    print(keyword)
    products = None
    product_count = 0

    if keyword:
        products = Product.objects.filter(product_name__icontains=keyword)
        product_count = products.count()
        print(products)

    context = {
        'product': products,
        "product_count": product_count
    }
    return render(request, "supuser/product.html", context)


@login_required(login_url='login')
def add_product(request):

    if request.method == 'POST':

        form = ProductEditForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product')
    else:
        form = ProductEditForm()

    context = {
        "form": form,
    }
    return render(request, 'supuser/add_product.html', context)


@login_required(login_url='login')
def edit_product(request, id):

    products = get_object_or_404(Product, id=id)

    if request.method == 'POST':

        form = ProductEditForm(request.POST, request.FILES, instance=products)
        if form.is_valid():
            form.save()
            return redirect('product')
        else:
            print(form.errors)
    else:
        print('notpost')
        form = ProductEditForm(instance=products)

    return render(request, 'supuser/edit_product.html', {'form': form, 'products': products})


@login_required(login_url='login')
def del_product(request, id):
    if request.method == 'POST':
        prod = Product.objects.get(id=id)
        prod.delete()
    return redirect('product')

# -----------------------------------------------------CATEGORY-MANAGE-------------------------------------------------------------------------------


@login_required(login_url='login')
def category_list(request):

    categories = category.objects.all()
    context = {
        "category": categories
    }
    return render(request, 'supuser/category.html', context)


@login_required(login_url='login')
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category')
    else:
        form = CategoryForm()
    context = {
        "form": form
    }
    return render(request, 'supuser/category.html', context)


@login_required(login_url='login')
def edit_category(request, id):

    categories = get_object_or_404(category, id=id)

    if request.method == 'POST':

        form = CategoryForm(request.POST, request.FILES, instance=categories)
        if form.is_valid():
            form.save()
            return redirect('category')
        else:
            print(form.errors)
    else:
        print('notpost')
        form = CategoryForm(instance=categories)

    return render(request, 'supuser/edit_category.html', {'form': form, 'categories': categories})


@login_required(login_url='login')
def del_category(request, id):
    if request.method == "POST":
        crt = category.objects.get(id=id)
        crt.delete()
    return redirect('category')
# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------


@login_required(login_url='login')
def orderslist(request):
    orders = Order.objects.all().order_by('-created_at')

    context = {
        'orders': orders,

    }
    return render(request, 'supuser/order_list.html', context)


@login_required(login_url='login')
def change_status(request, order_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
        except Order.DoesNotExist:
            pass

    return redirect('orderslist')


@login_required(login_url='login')
def order_details(request, order_id):
    print("hello")
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

    return render(request, 'supuser/order_detail.html', context)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='login')
def coupon(request):
    coupon = Coupon.objects.all().order_by('created_at')
    context = {
        'coupon': coupon,
    }
    return render(request, 'supuser/coupon.html', context)


@login_required(login_url='login')
def add_coupon(request):
    form = CouponForm()
    if request.method == "POST":
        form = CouponForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('coupon')
    else:
        form = CouponForm()
    context = {
        "form": form
    }
    return render(request, 'supuser/coupon.html', context)


def desable(request, id):
    if request.method == 'POST':
        pi = Coupon.objects.get(id=id)
        pi.active = False
        pi.save()
        return redirect('coupon')


def active(request, id):
    if request.method == 'POST':
        pi = Coupon.objects.get(id=id)
        pi.active = True
        pi.save()
        return redirect('coupon')
