# Python
from typing import Dict, Optional, List
# Django
from django.db.models import QuerySet, Q
from django.core.exceptions import ObjectDoesNotExist
# Local
from .models import Product, ProductCategory, ProductImage


def get_active_products() -> QuerySet:
    return Product.objects.filter(active=True)


def get_hidden_products() -> QuerySet:
    return Product.objects.filter(active=False)


def get_product_by_code(code: int) -> Optional[Product]:
    try:
        product = Product.objects.get(code=code)
    except ObjectDoesNotExist:
        return None
    return product


def get_active_products_by_category(category_name: str) -> QuerySet:
    try:
        category = ProductCategory.objects.get(name=category_name)
    except ObjectDoesNotExist:
        return None
    return Product.objects.filter(category=category)


def filter_products_by_query_params(query_params: Dict, active=True) -> QuerySet:
    queryset = get_active_products() if active else get_hidden_products()
    name_query = query_params.get("name")
    categories_query = query_params.get("categories")
    prices: Dict = query_params.get("prices")

    if name_query:
        queryset = queryset.filter(
            Q(name__contains=name_query) | Q(description__contains=name_query)
        )

    if categories_query:
        queryset = queryset.filter(category__name__in=categories_query)
    
    if prices is not None:
        min_price, max_price = prices.values()
        if min_price:
            queryset = queryset.exclude(price__lte=min_price)
        if max_price:
            queryset = queryset.exclude(price__gt=max_price)

    return queryset


def get_product_images(product: Product) -> List[ProductImage]:
    main_image = ProductImage(
        product=product,
        title=product.name,
        image=product.main_image
    )
    additional_images = [image for image in ProductImage.objects.filter(product=product)]
    additional_images.append(main_image)
    return additional_images


def get_category_by_name(category_name: str) -> Optional[ProductCategory]:
    try:
        category = ProductCategory.objects.get(name=category_name)
    except ObjectDoesNotExist:
        return None
    return category


def delete_product_by_code(code: int) -> bool:
    product = get_product_by_code(code)
    if product is not None:
        product.delete()
        return True
    else:
        return False


def toggle_product_visibility(code: int) -> bool:
    product = get_product_by_code(code)
    if product is not None:
        product.active = not product.active
        product.save()
        return True
    return False
