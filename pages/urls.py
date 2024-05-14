from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import HomePageView,ClientHomeView,AdmiHomeView,EmployeeHomeView, GoBack
from accounts.mixins import AdminRequiredMixin, ClientRequiredMixin


urlpatterns = [
    path("home", HomePageView.as_view(), name="home"),
    path("adminpanel/", AdmiHomeView.as_view(), name="admi_home"),
    path("employee/", EmployeeHomeView.as_view(), name="employee_home"),#Falta implementar
    path("", ClientHomeView.as_view(), name="client_home"),
    path("", GoBack.as_view(), name='go_back')
]
