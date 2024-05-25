from django.urls import path
from .views import EmployeeSignupView, EmployeeSuccessView


urlpatterns = [
    path("employee_signup/", EmployeeSignupView.as_view(), name="employee_signup"),
    path(
        "success/<int:employee_id>/",
        EmployeeSuccessView.as_view(),
        name="employee_success",
    ),
]

