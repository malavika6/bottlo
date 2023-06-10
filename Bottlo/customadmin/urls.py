from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.supuser,name='supuser'),
    path('product/',views.product_list,name='product'),
]
