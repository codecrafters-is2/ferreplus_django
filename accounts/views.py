from django.views import View
from django.views.generic import DetailView
from .forms import EmployeeUserCreationForm
from .models import EmployeeUser
from django.shortcuts import render, redirect
from django.contrib import messages
from .mixins import AdminRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from .models import CustomUser
from django.views.generic import TemplateView
from posts.models import Post

class EmployeeSignupView(AdminRequiredMixin, View):
    def get(self, request):
        form = EmployeeUserCreationForm()
        return render(request, "account/employee_signup.html", {"form": form})

    def post(self, request):
        form = EmployeeUserCreationForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(
                request,
                f"Empleado {employee.nombre} {employee.apellido} registrado exitosamente.",
            )
            return redirect("employee_success", employee_id=employee.id)
        return render(request, "account/employee_signup.html", {"form": form})


class EmployeeSuccessView(AdminRequiredMixin, View):
    def get(self, request, employee_id):
        employee = get_object_or_404(EmployeeUser, id=employee_id)
        return render(request, "account/employee_success.html", {"employee": employee})


# class UserDetailView(LoginRequiredMixin, View):
#    def get(self, request, user_id):
#        user = get_object_or_404(CustomUser, id=user_id)
#        return render(request, "account/user_detail.html", {"user": user})


class UserDetailWithPostsView(LoginRequiredMixin, TemplateView):
    template_name = "account/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get("user_id")
        user = get_object_or_404(CustomUser, id=user_id)
        context["user"] = user
        context["post_list"] = Post.objects.filter(author=user)
        return context
