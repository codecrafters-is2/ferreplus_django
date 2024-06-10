from django import template
from catalogo.models import Product

register = template.Library()

@register.inclusion_tag("components/product_card.html")
def show_product_card(product):
    displayable_product = {
        "name": product.name,
        "description": product.description,
        "image": product.main_image
    }
    return displayable_product