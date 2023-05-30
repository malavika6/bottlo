from django import forms
from .models import Account

class Registrationform(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={ 'placeholder':'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last name'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Email'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Mobile number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone_number','password']


         