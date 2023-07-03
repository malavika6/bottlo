from django import forms
from.models import Account
from django.contrib.auth.password_validation import validate_password

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Mobile number (e.g., +91XXXXXXXXXX)'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.startswith('+91') or len(phone_number) != 13:
            raise forms.ValidationError("Phone number must be in the format +91XXXXXXXXXX.")
        return phone_number

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)  # Django's built-in password validation
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code',
                               widget=forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Enter code here'})
    )

