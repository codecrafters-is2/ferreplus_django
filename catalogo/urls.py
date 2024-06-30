from django.urls import path
from .views import (
    ProductListView,
    ProductSearchView,
    ProductCreateView, 
    ProductImageUploadView,
    ProductDetailView,
    ProductDeleteView,
    ProductVisibilityToggleView,
    ProductDeleteSuccessMessageView,
    ProductVisibilityChangeSuccessMessageView
)

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("search/", ProductSearchView.as_view(), name="product_search"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("images/add/", ProductImageUploadView.as_view(), name="product_images_add"),
    path("product/<int:code>", ProductDetailView.as_view(), name="product_detail"),
    path("product/delete/<int:code>", ProductDeleteView.as_view(), name="product_delete"),
    path("product/visibility/<int:code>", ProductVisibilityToggleView.as_view(), name="product_visibility_toggle"),
    # Mensajes
    path("product/deleted/success", ProductDeleteSuccessMessageView.as_view(), name="product_delete_success"),
    path("product/visibility/success", ProductVisibilityChangeSuccessMessageView.as_view(), name="product_visibility_change_success")
]
