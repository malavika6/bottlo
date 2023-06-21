from django.shortcuts import render, redirect
from .forms import Registrationform,VerifyForm
from . models import Account
from django.contrib import messages,auth
from . import verify



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
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, phone_number=phone_number, email=email, password=password)
            user.save()
            verify.send(phone_number)
            messages.success(request, "Registration successfull")
            return redirect('verify_code')
    context = {
        'form': form,
    }
    return render(request, "account/signup.html", context)



def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if verify.check(request.user.phone_number, code):
                request.user.is_verified = True
                request.user.save()
                auth.login(request, request.user)
                return redirect('login')
    else:
        form = VerifyForm()
    return render(request, "account/verify.html", {'form': form})



def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)

        if email and password:
            myuser = auth.authenticate(email=email, password=password)
            print(email,password)

            if myuser is not None:
                auth.login(request, myuser)

                if request.user.is_superadmin:
                    return redirect('supuser')
                else:
                    return redirect('home')
            else:
                messages.error(request, "Invalid login credentials")
                print("Invalid login credentials")
        else:
            messages.error(request, "Email and password are required.")
            print("Email and password are required.")
    
    return render(request, "account/login.html")





def logout(request):
    return render(request, "account/logout.html")
