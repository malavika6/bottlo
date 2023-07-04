from django import forms
from store.models import Product
from category.models import category



class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = ["category_name", "slug", "description", "cat_image"]
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type here'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type here'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type here'}),
        }
    
    cat_image = forms.ImageField(label='Product Image', required=False)
    
    def clean_cat_image(self):
        cat_image = self.cleaned_data.get('cat_image')
        
        # Perform your custom validation logic here
        if cat_image and cat_image.size > 10 * 1024 * 1024:  # Example: restrict image size to 10MB
            raise forms.ValidationError("The image size should be less than 10MB.")
        
        return cat_image


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product_name", "slug", "description", "price",
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

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Perform image validation
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError(
                    'The image size should not exceed 5MB.')
            

        return image

    def clean(self):
        cleaned_data = super().clean()
        # Perform form field validations
        product_name = cleaned_data.get('product_name')
        slug = cleaned_data.get('slug')
        price = cleaned_data.get('price')
        stock = cleaned_data.get('stock')

        if not product_name:
            self.add_error('product_name', 'Product name is required.')

        if not slug:
            self.add_error('slug', 'Slug is required.')

        if not price or price <= 0:
            self.add_error('price', 'Price must be a positive number.')

        if not stock or stock < 0:
            self.add_error('stock', 'Stock must be a non-negative number.')

        return cleaned_data
