from django.shortcuts import render, redirect, get_object_or_404
from store.admin import ProductAdmin
from store.models import Product
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ProductEditForm, CategoryForm
from category.models import category
from order.models import Order, OrderProduct
from account.models import Account


def supuser(request):
    return render(request, "supuser/adminhome.html")

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


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


def product_list(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        "product": products,
    }

    return render(request, "supuser/product.html", context)


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


def del_product(request, id):
    if request.method == 'POST':
        prod = Product.objects.get(id=id)
        prod.delete()
    return redirect('product')

# -----------------------------------------------------CATEGOTY-MANAGE-------------------------------------------------------------------------------


def category_list(request):

    categories = category.objects.all()
    context = {
        "category": categories
    }
    return render(request, 'supuser/category.html', context)


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category')
    else:
        form = CategoryForm()
    context = {
        "form": form
    }
    return render(request, 'supuser/category.html', context)


def edit_category(request, id):

    categories= get_object_or_404(category, id=id)

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


def del_category(request, id):
    if request.method == "POST":
        crt = category.objects.get(id=id)
        crt.delete()
    return redirect('category')
# ------------------------------------------------------------------------------------------------------------------------------------------------------------


def orderslist(request):
    orders = Order.objects.all().order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'supuser/order_list.html', context)


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


def order_details(request, order_id):

    try:
        subtotal = 0
        ordr_product = OrderProduct.objects.filter(
            order__order_number=order_id)
        order = Order.objects.get(order_number=order_id)
        for i in ordr_product:
            if i.product.price:
                subtotal += i.product.price * i.quantity
            else:
                subtotal += i.product.price * i.quantity
        context = {
            'ordr_product': ordr_product,
            'order': order,
            'subtotal': subtotal
        }
    except Order.DoesNotExist:

        context = {
            'error_message': 'Order does not exist.'
        }

    return render(request, 'supuser/order_detail.html', context)
