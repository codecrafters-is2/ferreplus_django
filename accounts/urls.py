from django.urls import path
from accounts.views import ClientPasswordChangeView,CustomPasswordChangeView,ChangePasswordView

urlpatterns = [
    #path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('change-password/', ChangePasswordView.as_view(), name='password_change'),
]
