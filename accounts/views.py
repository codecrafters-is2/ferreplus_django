from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.mixins import ClientRequiredMixin


class ClientPasswordChangeView(ClientRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('password_change_done')

class CustomPasswordChangeView(ClientRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('password_change_done')
