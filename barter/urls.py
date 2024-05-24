from django.urls import path
from .views import BarterCreateView, BarterCreateSuccessView

urlpatterns = [
    path('barter/create/<int:post_id>/', BarterCreateView.as_view(), name='barter_request'),
    path('barter/success/', BarterCreateSuccessView.as_view(), name='barter_success'),
]
