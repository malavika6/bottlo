from django.shortcuts import render, get_object_or_404
from .models import Product,ProductImage
from category.models import category
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).prefetch_related('productimage_set')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).prefetch_related('productimage_set')
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
    return render(request, "store/store.html", context)



def product_details(request,category_slug,product_slug):
    
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        
    except Exception as e :
        raise e

    context ={
        "single_product":single_product,

    }    

    return render(request,'store/product_detail.html',context)
    
def search(request):
    keyword = request.GET.get('keyword')
    products = None
    product_count = 0
    
    if keyword:
       products = Product.objects.filter(product_name__icontains=keyword)
       product_count = products.count()
    
    context = {
        'product': products,
        "product_count" : product_count
    }
    return render(request, "store/store.html",context)