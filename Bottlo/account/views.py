from django.shortcuts import render
from .forms import Registrationform
from. models import Account

def signup(request):

    form = Registrationform()
    if request.method == 'POST':
        form = Registrationform(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(first_name = first_name, last_name = last_name, phone_number = phone_number, email = email, password = password)
            user.save()
    context = {
        'form':form,
    }
    return render(request,"account/signup.html",context)
def login(request):
    return render(request,"account/login.html")
def logout(request):
    return render(request,"account/logout.html")

