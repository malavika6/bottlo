from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.supuser, name='supuser'),

    path('product/', views.product_list, name='product'),
    path('product/add/',views.add_product,name="add_product"),
    path('product/edit/<int:id>', views.edit_product, name="edit_product"),
    path('product/del/<int:id>', views.del_product, name='del_product'),
    
    path('orderslist', views.orderslist, name="orderslist"),
    path('change_status/<int:order_id>', views.change_status, name="change_status"),
    path('order_details/<int:order_id>', views.order_details, name="order_details"),

]
