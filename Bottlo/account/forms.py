from django import forms
from .models import Account


class Registrationform(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Mobile number'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'email', 'phone_number', 'password']

    def clean(self):
        cleaned_data = super(Registrationform, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")
        
class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code',
                               widget=forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Enter code here'})
    )

