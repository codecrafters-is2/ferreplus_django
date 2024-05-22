from django.urls import path
from .views import EmployeeSignupView


urlpatterns = [
    path("employee_signup/", EmployeeSignupView.as_view(), name="employee_signup")
]
