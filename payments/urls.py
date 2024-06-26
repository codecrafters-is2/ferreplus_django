from django.urls import path
from .views import PackageSelectionView, PaymentSuccessView
app_name = 'payments'

urlpatterns = [
    path("<int:post_id>/package/", PackageSelectionView.as_view(), name="package-selection"),
    path("successful/purchase/", PaymentSuccessView.as_view(), name="success")

]