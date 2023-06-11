from django.shortcuts import render,redirect
from .forms import Registrationform
from. models import Account
from django.contrib import messages,auth

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
            messages.success(request,"Registration successfull")
            return redirect('login')
    context = {
        'form':form,
    }
    return render(request,"account/signup.html",context)
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        myuser = auth.authenticate(email=email, password=password)
        
        if myuser is not None:
            auth.login(request, myuser)
            
            if request.user.is_superadmin: 
                return redirect('supuser')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
    
    return render(request, "account/login.html")        
def logout(request):
    return render(request,"account/logout.html")

