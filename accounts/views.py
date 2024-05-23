from django.views.generic.edit import CreateView
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


def employee_success(request):
    return render(request, "account/employee_success.html")

    # model = EmployeeUser
    # template_name = "account/employee_signup.html"
    # form_class = EmployeeUserCreationForm

    # def form_valid(self, form):
    #    # Agrega el campo original_branch_id antes de guardar el formulario
    #    form.instance.original_branch_id = form.instance.branch.id
    #    ## Asigna el autor actualmente autenticado
    #    form.instance.author = self.request.user
    #
    #    #context = self.get_context_data()
    #    #image_formset = context['image_formset']
    #    #if image_formset.is_valid():
    #    #    self.object = form.save()
    #    #    image_formset.instance = self.object
    #    #    image_formset.save()
    #    #    uploaded_images = self.request.FILES.getlist('photo')
    #    #    for image in uploaded_images:
    #            # Crea una nueva instancia de ImagePost
    #    #        image_post = ImagePost(post=self.object, image=image)
    #            # Guarda la instancia en la base de datos
    #    #        image_post.save()
    #    return super().form_valid(form)
