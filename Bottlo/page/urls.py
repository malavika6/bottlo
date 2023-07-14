from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('profile/',views.profile,name='profile'),
    # path('profile/add_address',views.add_address,name='add_address'),
]