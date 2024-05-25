from django.urls import path
from .views import EmployeeSignupView, EmployeeSuccessView, UserDetailWithPostsView


urlpatterns = [
    path("employee_signup/", EmployeeSignupView.as_view(), name="employee_signup"),
    path(
        "success/<int:employee_id>/",
        EmployeeSuccessView.as_view(),
        name="employee_success",
    ),
    path("user/<int:user_id>/", UserDetailWithPostsView.as_view(), name="user_detail"),
]
