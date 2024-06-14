# Python
from typing import Dict, Optional
# Django
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView
# Local
from .models import Product
from .services import get_active_products, filter_products_by_query_params


class ProductListView(ListView):
    model = Product
    context_object_name = "product_list"
    template_name = "product_list.html"

    def get_queryset(self):
        return get_active_products()


class ProductSearchView(ListView):
    model = Product
    context_object_name = "product_list"
    template_name = "product_list.html"

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
        
        min_price = self._extract_float(self.request.GET.get("min_price"))
        max_price = self._extract_float(self.request.GET.get("max_price"))

        return {
            "name": name_query,
            "categories": categories_query,
            "prices": {
                "min_price": min_price,
                "max_price": max_price
            }
        }
    
    def _extract_float(self, str_value: str) -> Optional[str]:
        converted_value = None
        try:
            converted_value = float(str_value)
        except ValueError:
            return None
        return converted_value


class ProductCreateView(CreateView):
    model = Product
    def post():
        pass
