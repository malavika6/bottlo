from django.shortcuts import render, redirect, get_object_or_404
from store.admin import ProductAdmin
from store.models import product
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ProductEditForm
from category.models import category


def supuser(request):
    return render(request, "supuser/adminhome.html")


def product_list(request):
    products = product.objects.all().filter(is_available=True)

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
    categories = category.objects.all()

    context = {
        "category": categories,
        "form": form,
    }
    return render(request, 'supuser/add_product.html', context)

def edit_product(request, id):
    print("reach")
    
    products = get_object_or_404(product, id=id)
    print(products)

    if request.method == 'POST':
        print("post")

        form = ProductEditForm(request.POST,request.FILES, instance=products)
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
        prod = product.objects.get(id=id)
        prod.delete()
    return redirect('product')
