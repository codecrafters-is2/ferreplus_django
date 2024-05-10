from django.shortcuts import render
from django.views.generic import TemplateView
from accounts.models import CustomUser


class HomePageView(TemplateView):
    template_name = "home.html"
