from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView, TemplateView
from django.urls import reverse_lazy
from accounts.mixins import ClientRequiredMixin, EmployeeRequiredMixin
from .models import Barter, Post
from .forms import BarterForm
from django.db.models import Q
from accounts.models import EmployeeUser

class BarterCreateSuccessView(ClientRequiredMixin,TemplateView):
    template_name = 'temp_messages/barter_requested_successfuly.html'

class BarterCreateView(ClientRequiredMixin, CreateView):
    model = Barter
    form_class = BarterForm
    template_name = 'barter/barter_request.html'
    success_url = reverse_lazy('barter_success')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        requested_post = Post.objects.get(id=self.kwargs['post_id'])
        kwargs['user'] = self.request.user
        kwargs['requested_post'] = requested_post
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.requested_post_id = self.kwargs['post_id']
        return super().form_valid(form)

class BarterListView(ClientRequiredMixin, ListView):
    model = Barter
    template_name = 'barter/my_barters.html'
    context_object_name = 'barters'

    def get_queryset(self):
        user = self.request.user
        return Barter.objects.filter(
            Q(requesting_post__author=user) | Q(requested_post__author=user)
        ).distinct()
    
    def post(self, request, *args, **kwargs):
        selected_barter_id = request.POST.get('selected_barter_id')
        if selected_barter_id:
            return redirect('propose_turns', barter_id=selected_barter_id)
        return super().post(request, *args, **kwargs)
    
class BarterCancelView(ClientRequiredMixin, DeleteView):
    model = Barter
    template_name = 'barter_cancel.html'
    success_url = reverse_lazy('my_barters')
    
    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return super().delete(request, *args, **kwargs)
    
class CommittedBartersListView(EmployeeRequiredMixin, ListView):
    model = Barter
    template_name = 'barter/barters_record.html'
    
    def get_queryset(self):
        employee = EmployeeUser.objects.get(id=self.kwargs['employee_id'])
        return Barter.objects.filter(
            Q(branch=employee.branch) & (Q(state='committed') | Q(state='cancelled'))
        )

