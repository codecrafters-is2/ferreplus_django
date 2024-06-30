from django import forms
from catalogo.models import Product, ProductImage
from .validators import validate_non_existing_product
from .widgets import PRODUCT_CREATION_FORM_WIDGETS, IMAGE_CREATION_FORM_WIDGETS


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

    def clean(self):
        cleaned_data = super().clean()

        # Validación de código de producto
        product_code = cleaned_data.get("code")
        try:
            validate_non_existing_product(product_code)
        except Exception as e:
            self.add_error(
                "code",
                ("El código de producto ya existe en la base de datos"),
            )


class ProductImageCreationForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = [
            "product",
            "title",
            "image",
        ]
        widgets = IMAGE_CREATION_FORM_WIDGETS
        