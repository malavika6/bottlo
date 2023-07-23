from django import forms
from .models import Account,AddressBook


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
    code = forms.CharField(
        max_length=8,
        required=True,
        help_text='Enter code',
        widget=forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Enter code here'})
    )
    
    
class AddressForm(forms.ModelForm):
    # address =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-1', 'placeholder':'Enter Address'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Last Name'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'E-mail'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Phone Number'}))
    address_line_1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'House No & Locality *'}))
    address_line_2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'House No & Locality2 *'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'City'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'State'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Country'}))
    pincode = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2', 'placeholder':'Pincode'}))
    status = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    
    class Meta:
        model = AddressBook
        fields = ['first_name','last_name','phone','email','address_line_1','city','state','country','pincode','status']
        exclude = ("user",)