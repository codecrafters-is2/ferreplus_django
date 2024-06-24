from django.urls import path
from .views import (
    ProductListView,
    ProductSearchView,
    ProductCreateView, 
    ProductImageUploadView
)

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("search/", ProductSearchView.as_view(), name="product_search"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("images/add/", ProductImageUploadView.as_view(), name="product_images_add"),
]