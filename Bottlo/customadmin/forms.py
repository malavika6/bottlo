from django import forms
from store.models import product,ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ["product_name", "description", "price", "stock", "image", "is_available", "category"]
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
            'product_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'category': forms.Select(attrs={'class': 'form-control mb-3'}),
        }

    image = forms.ImageField(label='Product Image', required=True, error_messages={'required': 'Please upload an image.'}) 

class ImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["product", "image"]





    

