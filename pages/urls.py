from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import HomePageView,ClientHomeView,AdmiHomeView,EmployeeHomeView, GoBack, PasswordChangeSuccessView, EmailEditSuccessView
from accounts.mixins import AdminRequiredMixin, ClientRequiredMixin


urlpatterns = [
    path("home", HomePageView.as_view(), name="home"),
    path("adminpanel/", AdmiHomeView.as_view(), name="admi_home"),
    path(
        "employee/", EmployeeHomeView.as_view(), name="employee_home"
    ),  # Falta implementar
    path(
        "password/change/successful",
        PasswordChangeSuccessView.as_view(),
        name="password_change_success",
    ),
    path(
        "profile-edit-success",
        EmailEditSuccessView.as_view(),
        name="profile_edit_success",
    ),
    path("", ClientHomeView.as_view(), name="client_home"),
    path("", GoBack.as_view(), name="go_back"),
]
