from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView, TemplateView
from django.urls import reverse_lazy
from accounts.mixins import ClientRequiredMixin
from .models import Barter, Post
from .forms import BarterForm
from django.contrib import messages
from django.db.models import Q

class BarterCreateSuccessView(ClientRequiredMixin,TemplateView):
    template_name = 'temp_messages/barter_requested_successfuly.html'

class BarterCreateView(ClientRequiredMixin, CreateView):
    model = Barter
    form_class = BarterForm
    template_name = 'barter/barter_request.html'
    success_url = reverse_lazy('barter_success')  # Reemplaza con la URL de éxito adecuada

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
    
class BarterCancelView(ClientRequiredMixin, DeleteView):
    model = Barter
    template_name = 'barter_cancel.html'
    success_url = reverse_lazy('my_barters')
    
    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return super().delete(request, *args, **kwargs)