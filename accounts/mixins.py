from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages


class AdminRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="admi").exists():
            return super().dispatch(request, *args, **kwargs)
        return redirect('home')

class ClientRequiredMixin(LoginRequiredMixin):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="client").exists():
            return super().dispatch(request, *args, **kwargs)
        # Registro de un mensaje para ayudar a depurar el redireccionamiento
        print("Acceso denegado: El usuario no pertenece al grupo de clientes.")
        return redirect('home')

class EmployeeRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="employee").exists():
            return super().dispatch(request, *args, **kwargs)
        return redirect('home')
