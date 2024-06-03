from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView,DetailView, View
from accounts.mixins import EmployeeRequiredMixin
from posts.models import Post, Question
from accounts.models import EmployeeUser

class PostListView(EmployeeRequiredMixin,ListView):
    model = Post
    template_name = "posts/list/post_list_employee.html"
    context_object_name = "post_list"
    
    def get_queryset(self):
        # Obtener todas las publicaciones
        queryset = super().get_queryset().filter(status="available")
        user = self.request.user
        print("Antes de entrar")
        # Obtener el EmployeeUser relacionado
        try:
            employee_user = EmployeeUser.objects.get(username=user.username)
            # Filtrar las publicaciones por la branch del empleado
            queryset = queryset.filter(branch=employee_user.branch)
        except EmployeeUser.DoesNotExist:
            # Manejar el caso donde no se encuentre un EmployeeUser relacionado
            queryset = queryset.none()
        return queryset

class PostDetailView(EmployeeRequiredMixin,DetailView):
    model = Post
    template_name = "posts/detail/post_detail_employee.html"


class DeleteQuestionView(EmployeeRequiredMixin, View):
    model = Question
    
    def post(self, request, *args, **kwargs):
        question_id = kwargs.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        post_id = question.post.pk
        question.delete()
        return redirect('post_detail_employee', pk=post_id)


class DeleteAnswerView(EmployeeRequiredMixin, View):
    model = Question
    
    def post(self, request, *args, **kwargs):
        question_id = kwargs.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        question.answer = None
        question.save()
        return redirect('post_detail_employee', pk=question.post.pk)

