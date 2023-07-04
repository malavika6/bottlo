from django.contrib import admin
from .models import Product,ProductImage

# Register your models here.
class PictureInline(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [PictureInline]
    

    list_display =('product_name','slug','price','stock','category','modified_date','is_available')
    prepopulated_fields={'slug':('product_name',)}


admin.site.register(Product,ProductAdmin)





