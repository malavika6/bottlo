from django import forms
from store.models import product


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ["product_name","slug", "description", "price",
                  "stock", "image", "is_available", "category"]
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'slug': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'category': forms.Select(attrs={'class': 'form-control mb-3'}),
        }

    image = forms.ImageField(label='Product Image', required=False)
