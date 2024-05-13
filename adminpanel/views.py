from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from branches.models import Branch
from .forms import BranchForm
from accounts.mixins import AdminRequiredMixin

class AdminPanelView(AdminRequiredMixin, TemplateView):
    template_name = 'adminpanel.html'

class BranchListView(AdminRequiredMixin, ListView):
    model = Branch
    template_name = 'show_branches.html'
    context_object_name = 'branches'

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
    