from django.shortcuts import render
from store.models import product



def supuser(request):
    return render(request,"supuser/adminhome.html")


def product_list(request):
    products = product.objects.all().filter(is_available=True)
    
    context = {
        "product" : products,  
          }

    return render(request,"supuser/product.html",context)
