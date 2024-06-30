# Django
from django.core.exceptions import ValidationError
# Local
from catalogo.services import get_product_by_code


def validate_non_existing_product(code):
    if get_product_by_code(code) is not None:
        raise ValidationError(
            "El producto ya existe en la base de datos",
            params={"value": code},
        )
