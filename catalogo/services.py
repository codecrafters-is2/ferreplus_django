# Python
from typing import Dict
# Django
from django.db.models import QuerySet, Q
from django.core.exceptions import ObjectDoesNotExist
# Local
from .models import Product, ProductCategory


def get_active_products() -> QuerySet:
    return Product.objects.filter(active=True)


def get_active_products_by_category(category_name: str) -> QuerySet:
    try:
        category = ProductCategory.objects.get(name=category_name)
    except ObjectDoesNotExist:
        return None
    return Product.objects.filter(category=category)


def filter_products_by_query_params(query_params: Dict) -> QuerySet:
    queryset = get_active_products()
    name_query = query_params.get("name")
    categories_query = query_params.get("categories")
    prices: Dict = query_params.get("price")

    if name_query:
        queryset = queryset.filter(
            Q(name__contains=name_query) | Q(description__contains=name_query)
        )

    if categories_query:
        queryset = queryset.filter(category__in=categories_query)

    if prices:
        min_price, max_price = prices.values()
        if min_price:
            queryset = queryset.exclude(price__lte=min_price)
        if max_price:
            queryset = queryset.exclude(price__gt=max_price)

    return queryset

def get_product_images(product: Product) -> QuerySet:
    return ProductImage.objects.filter(product=product)
