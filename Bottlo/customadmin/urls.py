from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.supuser,name='supuser'),
    path('product/',views.product_list,name='product'),
    path('product/del/<int:id>',views.del_product,name='del_product'),
]
