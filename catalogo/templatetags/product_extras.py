# Python
from typing import Dict, List
# Django
from django import template
# Local
from catalogo.models import Product, ProductCategory
from catalogo.forms import ProductImageCreationForm

register = template.Library()

@register.inclusion_tag("components/product_card.html")
def show_product_card(product):
    displayable_product = {
        "name": product.name,
        "description": product.description,
        "image": product.main_image,
        "price": product.price
    }
    return displayable_product


@register.inclusion_tag("ui_components/categories_selector.html")
def show_catalog_categories_selector() -> Dict:
    categories_list = []
    raw_categories = ProductCategory.objects.all()
    for category in raw_categories:
        categories_list.append({
            "name": category.name,
            "description": category.description,
            "db_name": category.name,
            "image": category.image
        })

    return { "categories": categories_list }


@register.inclusion_tag("components/product_images_form.html")
def show_product_images_add_widget(submit_url) -> Dict:
    image_form = ProductImageCreationForm()
    return { 
        "image_form": image_form,
        "submit_url": submit_url
    }

@register.inclusion_tag("components/product_carousel.html")
def show_product_carousel(images: List) -> Dict:
    displayable_images = list()
    number = 0
    for image in images:
        displayable_images.append({
            "title": image.title,
            "image": image.image,
            "number": number
        })
        number += 1
    return {"images": displayable_images}
