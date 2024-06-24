from django import forms

PRODUCT_CREATION_FORM_WIDGETS = {
    "code": forms.NumberInput(
        attrs={
            "class": "form-control product-creation-input",
            "placeholder": "Código"
        }
    ),
    "name": forms.TextInput(
        attrs={
            "class": "form-control product-creation-input",
            "placeholder": "Nombre"
        }
    ),
    "brand": forms.TextInput(
        attrs={
            "class": "form-control product-creation-input",
            "placeholder": "Marca"
        }
    ),
    "model": forms.TextInput(
        attrs={
            "class": "form-control product-creation-input",
            "placeholder": "Modelo"
        }
    ),
    "description": forms.TextInput(
        attrs={
            "class": "form-control product-creation-input",
            "placeholder": "Descripción"
        }
    ),
    "price": forms.NumberInput(
        attrs={
            "class": "form-control product-creation-input",
            "placeholder": "Precio"
        }
    ),
    "category": forms.Select(
        attrs={
            "class": "form-control product-creation-input",
            "placeholder": "Categoría",
        }
    ),
    "stock": forms.NumberInput(
        attrs={
            "class": "form-control product-creation-input",
            "placeholder": "Stock",
        }
    ),
    "main_image": forms.FileInput(
        attrs={
            "class": "form-control product-creation-input",
            "placeholder": "Imagen",
        }
    )
}

IMAGE_CREATION_FORM_WIDGETS = {
    "image": forms.FileInput(
        attrs={
            "class": "form-control image-creation-input",
            "placeholder": "imagen",
        }
    ),
    "title": forms.TextInput(
        attrs={
            "class": "form-control image-creation-input",
            "placeholder": "Título"
        }
    ),
    "product": forms.NumberInput(
        attrs={
            "class": "form-control image-creation-input",
            "id": "product-code",
            "placeholder": "producto",
            "style": "display: none;"
        }
    )
}
