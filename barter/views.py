from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from accounts.mixins import ClientRequiredMixin
from .models import Barter, Post
from .forms import BarterForm
from django.views.generic import TemplateView

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
