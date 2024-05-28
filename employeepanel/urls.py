from django.urls import path
from .views import EmployeePanelView

urlpatterns = [
    path("", EmployeePanelView.as_view(), name="employeepanel"),
]
