from django.urls import path
from .views import BarterCreateView, BarterCreateSuccessView, BarterListView, BarterCancelView

urlpatterns = [
    path('barter/create/<int:post_id>/', BarterCreateView.as_view(), name='barter_request'),
    path('barter/success/', BarterCreateSuccessView.as_view(), name='barter_success'),
    path('', BarterListView.as_view(), name='my_barters'),
    path('cancel/<int:pk>/', BarterCancelView.as_view(), name='barter_cancel'),
]
