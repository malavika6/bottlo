from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.supuser, name='supuser'),
    
    path('usermanagement/', views.usermanagement, name='usermanagement'),
    path('usermanagement/block/<int:id>/',views.block_user, name='block_user'),
    path('usermanagement/unblock/<int:id>/',views.unblock_user, name='unblock_user'),

    path('searchs/',views.search,name='searchs'),
    path('product/', views.product_list, name='product'),
    path('category/<slug:category_slug>/', views.product_list, name="product_list_by_category"),
    path('product/add/',views.add_product,name="add_product"),
    path('product/edit/<int:id>', views.edit_product, name="edit_product"),
    path('product/del/<int:id>', views.del_product, name='del_product'),
    
    path('category/', views.category_list, name='category'),
    path('category/add/',views.add_category,name="add_category"),
    path('category/edit/<int:id>', views.edit_category, name="edit_category"),
    path('category/del/<int:id>', views.del_category, name='del_category'),
    
    path('coupon/',views.coupon,name='coupon'),
    
    path('orderslist', views.orderslist, name="orderslist"),
    path('change_status/<int:order_id>', views.change_status, name="change_status"),
    path('order_details/<int:order_id>', views.order_details, name="order_details"),

]
