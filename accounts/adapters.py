from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class FerreplusAccountAdapter(DefaultAccountAdapter):

    def get_password_change_redirect_url(self, request):
        return reverse("password_change_success")
