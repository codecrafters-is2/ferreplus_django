# Python
from typing import Dict
# Django
from django.views.generic import ListView
# Local
from .models import Product
from .services import filter_products_by_query_params


class ProductSearchView(ListView):
    model = Product
    context_object_name = "product_list"
    template_name = ""

    def get_queryset(self):
        query_params = self._get_query_params()
        return filter_products_by_query_params(query_params)

    def _get_query_params(self) -> Dict:
        name_query = self.request.GET.get("name")
        raw_categories_query = self.request.GET.get("categories")

        if raw_categories_query:
            categories_query = raw_categories_query.split(",")
        else:
            categories_query = ""

        min_price = self.request.GET.get("min-price")
        max_price = self.request.GET.get("max-price")

        return {
            "name": name_query,
            "categories": categories_query,
            "prices": {
                "min_price": float(min_price),
                "max_price": float(max_price)
            }
        }
