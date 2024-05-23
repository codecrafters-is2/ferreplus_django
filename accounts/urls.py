from django.urls import path
from .views import employeeSignupView, employee_success


urlpatterns = [
    path("employee_signup/", employeeSignupView, name="employee_signup"),
    path("success/", employee_success, name="employee_success")
]
