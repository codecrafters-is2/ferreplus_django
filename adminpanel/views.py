from django.db.models.query import QuerySet
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from branches.models import Branch
from .forms import BranchForm
from accounts.mixins import AdminRequiredMixin
from django.views import View
from accounts.forms import EmployeeUserCreationForm
from accounts.models import EmployeeUser
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404

class AdminPanelView(AdminRequiredMixin, TemplateView):
    template_name = 'adminpanel.html'

class BranchListView(AdminRequiredMixin, ListView):
    model = Branch
    template_name = 'show_branches.html'
    context_object_name = 'branches'

    def get_queryset(self):
         return Branch.active_objects.all()

class BranchCreateView(AdminRequiredMixin, CreateView):
    model = Branch
    form_class = BranchForm
    template_name = 'register_new_branch.html'
    success_url = reverse_lazy('show_branches')

class BranchUpdateView(AdminRequiredMixin, UpdateView):
    model = Branch
    form_class = BranchForm
    template_name = 'edit_branch.html'
    success_url = reverse_lazy('show_branches')

    def get_form_class(self):
            return RestrictedBranchForm 

class RestrictedBranchForm(AdminRequiredMixin, BranchForm):
    class Meta(BranchForm.Meta):
        exclude = ['city', 'postal_code'] 

class BranchDeleteView(AdminRequiredMixin, DeleteView):
    model = Branch
    template_name = 'confirm_branch_removal.html'
    success_url = reverse_lazy('show_branches')

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return super().delete(request, *args, **kwargs)


class EmployeeSignupView(AdminRequiredMixin, View):
    def get(self, request):
        form = EmployeeUserCreationForm()
        return render(request, "account/employee_signup.html", {"form": form})

    def post(self, request):
        form = EmployeeUserCreationForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(
                request,
                f"Empleado {employee.nombre} {employee.apellido} registrado exitosamente.",
            )
            return redirect("employee_success", employee_id=employee.id)
        return render(request, "account/employee_signup.html", {"form": form})


class EmployeeSuccessView(AdminRequiredMixin, View):
    def get(self, request, employee_id):
        employee = get_object_or_404(EmployeeUser, id=employee_id)
        return render(request, "account/employee_success.html", {"employee": employee})
