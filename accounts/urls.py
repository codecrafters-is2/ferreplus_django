from django.urls import path
from accounts.views import ClientPasswordChangeView,CustomPasswordChangeView

urlpatterns = [
    path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
