from django.shortcuts import render,redirect
from store.models import product
from django.http import HttpResponse,HttpResponseRedirect



def supuser(request):
    return render(request,"supuser/adminhome.html")


def product_list(request):
    products = product.objects.all().filter(is_available=True)
    
    context = {
        "product" : products,  
          }

    return render(request,"supuser/product.html",context)

def del_product(request,id):
    if request.method=='POST':
        prod = product.objects.get(id=id)
        prod.delete()
    return redirect('product')


