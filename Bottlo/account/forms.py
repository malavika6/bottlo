from django import forms
from .models import Account

class Registrationform(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username','email','phone_number','password']