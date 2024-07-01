# Python
from typing import Dict, List
# Django
from django import template
from django.urls import reverse
# Local
from catalogo.models import Product, ProductCategory
from catalogo.forms import ProductImageCreationForm

register = template.Library()


@register.inclusion_tag("components/product_card.html")
def show_product_card(product, user) -> Dict:
    detail_url = reverse("product_detail", kwargs={"code":product.code})
    displayable_product = {
        "pk": product.pk,
        "name": product.name,
        "code": product.code,
        "detail_url": detail_url,
        "description": product.description,
        "image": product.main_image,
        "price": product.price,
        "user": user  # Por alguna razón el contexto de usuario no llega al inclusion tag
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


@register.inclusion_tag("components/delete_button.html")
def show_product_delete_button(product_code: int, size: str) -> Dict:
    delete_url = reverse("product_delete", kwargs={"code": product_code})
    return {
        "url": delete_url,
        "product_code": product_code,
        "size": size
    }


@register.inclusion_tag("components/delete_modal.html")
def show_product_delete_modal() -> Dict:
    pass


@register.inclusion_tag("components/visibility_button.html")
def show_visibility_toggle_button(product_code: int, size: str) -> Dict:
    visibility_toggle_url = reverse("product_visibility_toggle", kwargs={"code": product_code})
    return {
        "url": visibility_toggle_url,
        "product_code": product_code,
        "size": size
    }


@register.inclusion_tag("components/visibility_modal.html")
def show_product_visibility_toggle_modal(message: str, button_label: str) -> Dict:
    return {
        "message": message,
        "button_label": button_label
    }


@register.inclusion_tag("components/edit_button.html")
def show_product_edit_button(pk: int) -> Dict:
    edit_url = reverse("product_edit", kwargs={"pk": pk})
    return {
        "edit_url": edit_url
    }
