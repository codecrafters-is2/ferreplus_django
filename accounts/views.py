from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import CustomUser
from django.views.generic import TemplateView
from posts.models import Post


class UserDetailWithPostsView(LoginRequiredMixin, TemplateView):
    template_name = "account/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get("user_id")
        user = get_object_or_404(CustomUser, id=user_id)
        context["user_post"] = user
        context["post_list"] = Post.objects.filter(author=user)
        context["user"] = self.request.user
        return context
