from django import forms
from catalogo.models import Product, ProductImage
from .widgets import PRODUCT_CREATION_FORM_WIDGETS

class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "code",
            "name",
            "brand",
            "model",
            "description",
            "price",
            "category",
            "stock",
            "main_image",
            ]
        widgets = PRODUCT_CREATION_FORM_WIDGETS


class ProductImageCreationForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = [
            "title",
            "image",
        ]
        
