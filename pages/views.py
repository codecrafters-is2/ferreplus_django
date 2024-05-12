from django.shortcuts import render
from django.views.generic import TemplateView
from accounts.models import CustomUser
from posts.models import Post


class HomePageView(TemplateView):
    #model = Post -> No es necesario por la redefinicion del metodo
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()
        return context
