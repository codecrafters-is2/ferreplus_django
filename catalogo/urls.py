from django.urls import path
from .views import ProductListView, ProductSearchView

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("search/", ProductSearchView.as_view(), name="product_search"),
]