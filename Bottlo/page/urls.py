from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('profile/',views.profile,name='profile'),
    path('order_detail/<int:order_id>/',views.order_detail,name="order_detail"),
    path('order_detail/cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    # path('profile/add_address',views.add_address,name='add_address'),
]