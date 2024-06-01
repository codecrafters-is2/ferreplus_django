from django.views.generic import ListView,TemplateView
from accounts.mixins import EmployeeRequiredMixin
from posts.models import Post

class PostListView(EmployeeRequiredMixin,ListView):
    model = Post
    template_name = "posts/post_list_employee.html"
    context_object_name = "post_list"
    
    def get_queryset(self):
        # Obtener todas las publicaciones
        queryset = super().get_queryset()
        queryset = queryset.filter(status="available")
        return queryset


