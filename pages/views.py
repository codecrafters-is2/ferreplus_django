from django.shortcuts import render
from django.views.generic import TemplateView
from accounts.models import CustomUser
from django.contrib.auth import get_user_model


class HomePageView(TemplateView):
    template_name = "home.html"
