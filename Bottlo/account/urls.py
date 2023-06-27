from django.urls import path, include
from . import views


urlpatterns = [
    
    
    path('signup/', views.signup, name='signup'),
    path('verify/', views.verify_code, name='verify_code'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
     path('reset_password/<uidb64>/<token>/',views.reset_password,name='reset_password'),
    
]
