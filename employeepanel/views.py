# Django
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView,DetailView, View
from django.db.models import Q
# Local
from accounts.mixins import EmployeeRequiredMixin
from accounts.models import EmployeeUser
from posts.models import Post, Question
from .services import get_employee_post_list

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


class PostSearchView(EmployeeRequiredMixin, ListView):
    model = Post
    context_object_name = "post_list"
    template_name = "posts/list/post_list_employee.html"

    def get_queryset(self):
        queryset = None
        try:
            employee = EmployeeUser.objects.filter(username=self.request.user.username)[0]
            queryset = get_employee_post_list(employee)
            title_query = self.request.GET.get("title")
            print(title_query)
            if title_query:
                queryset = queryset.filter(
                    Q(title__contains=title_query) | Q(body__contains=title_query)
                )

        except Exception as error:
            print(error)

        return queryset

    def get_context_data(self, **kwargs):
        """ Datos adicionales para los filtros """
        context = super().get_context_data()
        title_query = self.request.GET.get("title")
        context["title_query"] = title_query
        return context
