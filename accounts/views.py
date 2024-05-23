from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from .forms import EmployeeUserCreationForm
from .models import EmployeeUser
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import request


def employeeSignupView(request):
    if request.method == "POST":
        form = EmployeeUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Pasando el request al método save
            messages.success(request, "Empleado registrado exitosamente.")
            return redirect(
                "employee_success"
            )  # Redirigir a una URL llamada 'employee_success'
    else:
        form = EmployeeUserCreationForm()

    return render(request, "account/employee_signup.html", {"form": form})


# class EmployeeSuccess(DetailView):  # Visualización de la publicación propia
#    model = EmployeeUser
#    template_name = "account/employee_success.html"


def employee_success(request):
    return render(request, "account/employee_success.html")
