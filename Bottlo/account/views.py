from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import Registrationform, VerifyForm
from . models import Account
from django.contrib import messages, auth
from . import verify
from django.contrib.auth.decorators import login_required
from cart.models import Cart, Cartitem
from cart.views import _cart_id

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests


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
            request.session['email'] = email
            verify.send(phone_number)
            # messages.success(request, "Registration successfull")
            return redirect('verify_code')
    context = {
        'form': form,
    }
    return render(request, "account/signup.html", context)


# def verify_code(request):
#     if request.method == 'POST':
#         form = VerifyForm(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data['code']
#             user = Account._default_manager.get(
#                 email=request.session.get('email'))
#             if verify.check(user.phone_number,code):
#                 user.is_active = True
#                 user.is_verified = True
#                 user.save()
#                 print("hidishdl")
#                 return redirect('login')
#     else:
#         form = VerifyForm()
#     return render(request, 'account/verify.html', {'form': form})

def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user = Account._default_manager.get(
                email=request.session.get('email'))
            if verify.check(user.phone_number,code):
                user.is_active = True
                user.is_verified = True
                user.save()
                return redirect('login')
    else:
        form = VerifyForm()
    return render(request, 'account/verify.html', {'form': form})

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            myuser = auth.authenticate(email=email, password=password)

            if myuser is not None:

                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = Cartitem.objects.filter(
                        cart=cart).exists()
                    if is_cart_item_exists:
                        cart_items = Cartitem.objects.filter(cart=cart)
                        for item in cart_items:
                            item.user = myuser 
                            item.save()
                except:
                    pass

                auth.login(request, myuser)

                if request.user.is_superadmin:
                    return redirect('supuser')
                else:
                    return redirect('home')
            else:
                messages.error(request, "Invalid login credentials")
                print("Invalid login credentials")
        else:
            # messages.error(request, "Email and password are required.")
            print("Email and password are required.")

    return render(request, "account/login.html")


def forgotpassword(request):
    print("hiiiiiii")
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'ghostcart : Reset your password'
            message = render_to_string('account/reset_password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            print(to_email)
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(
                request, 'Password reset email has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request, "Account Does't Exists!!!")
            return redirect('forgotpassword')
    return render(request, 'account/forgotpassword.html')


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password.!')
        return redirect('resetpassword')
    else:
        messages.error(request, 'Sorry, the activation link has expired.!')
        return redirect('login')


def resetpassword(request):

    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['Confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "sucessfully reset password")
            return redirect('login')

        else:
            messages.error(request, "Passwords are not match")
            return redirect('resetpassword')
    else:
        return render(request, 'account/resetpassword.html')


@login_required(login_url='login')
def logout(request):
    if 'email' in request.session:
        request.session.flush
    auth.logout(request)
    messages.success(request, "logout sucessfully")
    return redirect("login")



