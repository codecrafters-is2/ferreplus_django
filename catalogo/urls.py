from django.urls import path
from .views import (
    ProductListView,
    ProductSearchView,
    ProductCreateView, 
    ProductImageUploadView,
    ProductDetailView,
    ProductDeleteView,
    ProductDeleteSuccessMessageView
)

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("search/", ProductSearchView.as_view(), name="product_search"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("images/add/", ProductImageUploadView.as_view(), name="product_images_add"),
    path("product/<int:code>", ProductDetailView.as_view(), name="product_detail"),
    path("product/delete/<int:code>", ProductDeleteView.as_view(), name="product_delete"),
    # Mensajes
    path("product/deleted/success", ProductDeleteSuccessMessageView.as_view(), name="product_delete_success")
]
