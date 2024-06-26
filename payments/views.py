from django.views.generic import FormView, TemplateView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from .forms import PaymentForm
from posts.models import Post
from accounts.mixins import ClientRequiredMixin

class PackageSelectionView(ClientRequiredMixin, FormView):
    template_name = 'payments/package-selection.html'
    form_class = PaymentForm
    success_url = reverse_lazy('payments:success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, id=self.kwargs['post_id'])
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['post_id'] = self.kwargs['post_id']
        return kwargs

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        package = form.cleaned_data['package']
        post.change_package(package)
        return super().form_valid(form)

class PaymentSuccessView(ClientRequiredMixin, TemplateView):
    template_name = 'payments/success.html'
