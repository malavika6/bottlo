from django.urls import path
from . import views

urlpatterns = [
    path('place_order/',views.place_order,name="place_order"),
    path('order_payment/',views.order_payment,name="order_payment"),
    
]

