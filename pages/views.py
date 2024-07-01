from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from accounts.mixins import ClientRequiredMixin,AdminRequiredMixin,EmployeeRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, get_object_or_404
from django.views import View
from branches.models import Branch
from accounts.models import EmployeeUser


class GoBack(View):
    def get(self, request, *args, **kwargs):
        # Obtener la URL de la página anterior
        previous_url = request.META.get('HTTP_REFERER')
        if previous_url:
            return HttpResponseRedirect(previous_url)
        else:
            # Si no hay una página anterior, redirigir a una URL predeterminada
            return HttpResponseRedirect(reverse('home'))


class HomePageView(TemplateView):
    # model = Post -> No es necesario por la redefinicion del metodo
    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if user.groups.filter(name='client').exists():
            # NUEVO ----
            if request.method == "POST" and "accept_terms" in request.POST:
                request.user.accepted_terms = True
                request.user.save()
                return redirect("client_home")
            return render(request, "client_home.html", {"show_modal": not request.user.accepted_terms})
            # -----
            # return redirect('client_home')
        elif user.groups.filter(name='employee').exists():
            return redirect("employee_home")
        elif user.groups.filter(name='admi').exists():
            return redirect('admi_home')
        else:
            return super().dispatch(request, *args, **kwargs)
    # Por si quiero mostrar publicaciones:
    # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['post_list'] = Post.objects.all()
    #    return context


class ClientHomeView(ClientRequiredMixin,TemplateView):
    #model = Post -> No es necesario por la redefinicion del metodo
    template_name = "client_home.html"


class AdmiHomeView(AdminRequiredMixin,TemplateView):
    template_name = "adminpanel.html"


class EmployeeHomeView(EmployeeRequiredMixin,TemplateView):
    # template_name = "employee_home.html"
    def get(self, request):
        employee = EmployeeUser.objects.get(username=request.user.username)
        return render(request, "employee_home.html", {"employee": employee})


class PasswordChangeSuccessView(TemplateView):
    template_name = "temp_messages/password_change_successful.html"

class EmailEditSuccessView(TemplateView):
    template_name = "temp_messages/email_change_successful.html"


class ShowContactInfo(ListView):
    model = Branch
    template_name = "contact_info.html"
    context_object_name = "branches"


def show_contact_info(request):
    branches = Branch.objects.all()
    branches_by_city = {}

    if not branches:
        branches_by_city = None
    else:
        for branch in branches:
            city = branch.city
            if city in branches_by_city:
                branches_by_city[city].append(branch)
            else:
                branches_by_city[city] = [branch]

    context = {'branches_by_city': branches_by_city}
    return render(request, "contact_info.html", context)
