from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.store,name='store'),
    path('category/<slug:category_slug>/', views.store, name="product_by_category"),
]