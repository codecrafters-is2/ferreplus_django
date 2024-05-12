from django.views.generic import ListView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from branches.models import Branch
from posts.models import Post
from .forms import BranchForm

class BranchListView(ListView):
    model = Branch
    template_name = 'show_branches.html'
    context_object_name = 'branches'

class BranchCreateView(CreateView):
    model = Branch
    form_class = BranchForm
    template_name = 'register_new_branch.html'
    success_url = reverse_lazy('show_branches')

class BranchUpdateView(UpdateView):
    model = Branch
    form_class = BranchForm
    template_name = 'edit_branch.html'
    success_url = reverse_lazy('show_branches')

class BranchDeleteView(DeleteView):
    model = Branch
    template_name = 'confirm_branch_removal.html'
    success_url = reverse_lazy('show_branches')
    
    #def post(self, request, *args, **kwargs):
    #    # Lógica para eliminar el Branch y cambiar el estado del Post
    #    branch = self.get_object()
    #    branch.delete()  # Elimina el Branch
#
    #    # Actualiza el estado de los Posts relacionados
    #    posts = Post.objects.filter(branch=branch)
    #    for post in posts:
    #        post.cambiarEstadoDelPost()
#
    #    return super().post(request, *args, **kwargs)