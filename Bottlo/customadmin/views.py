from django.shortcuts import render,redirect,get_object_or_404
from store.models import product
from django.http import HttpResponse,HttpResponseRedirect
from .forms import ProductForm




def supuser(request):
    return render(request,"supuser/adminhome.html")


def product_list(request):
    products = product.objects.all().filter(is_available=True)
    
    context = {
        "product" : products,  
          }

    return render(request,"supuser/product.html",context)

def edit_product(request,id):
    Product = get_object_or_404(product, id=id)
    if request.method == "POST":
        
        product_form = ProductForm(request.POST, request.FILES, instance=Product)
        if product_form.is_valid():
            product_form.save()
            return redirect('productmanage')
    else:
        product_form = ProductForm(instance=Product)

    context = {
        "product_form": product_form
    }
    return render(request, 'supuser/edit_product.html', context)


def del_product(request,id):
    if request.method=='POST':
        prod = product.objects.get(id=id)
        prod.delete()
    return redirect('product')


