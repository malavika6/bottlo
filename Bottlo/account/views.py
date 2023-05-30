from django.shortcuts import render
from .forms import Registrationform

def signup(request):
    form = Registrationform()
    context = {
        'form':form,
    }
    return render(request,"account/signup.html",context)
def login(request):
    return render(request,"account/login.html")
def logout(request):
    return render(request,"account/logout.html")

