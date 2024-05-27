from django.shortcuts import render
from django.views.generic import TemplateView
from accounts.mixins import EmployeeRequiredMixin


## Create your views here.
#class EmployeePanelView(EmployeeRequiredMixin, TemplateView):
#    template_name = "employee_home.htm"
