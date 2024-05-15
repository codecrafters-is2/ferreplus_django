from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView
#from accounts.models import CustomUser
#from posts.models import Post
from accounts.mixins import ClientRequiredMixin,AdminRequiredMixin,EmployeeRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.views import View

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
    #model = Post -> No es necesario por la redefinicion del metodo
    template_name = "home.html"
    
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='client').exists():
            return redirect('client_home')
        elif user.groups.filter(name='employee').exists():
            return redirect('employee_home')
        elif user.groups.filter(name='admi').exists():
            return redirect('admi_home')
        else:
            return super().dispatch(request, *args, **kwargs)
    #Por si quiero mostrar publicaciones:
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['post_list'] = Post.objects.all()
    #    return context

class ClientHomeView(ClientRequiredMixin,TemplateView):
    #model = Post -> No es necesario por la redefinicion del metodo
    template_name = "client_home.html"
    

class AdmiHomeView(AdminRequiredMixin,TemplateView):
    template_name = "adminpanel.html"


class EmployeeHomeView(EmployeeRequiredMixin,TemplateView):
    template_name = "employee_home.html"


class PasswordChangeSuccessView(TemplateView):
    template_name = "temp_messages/password_change_successful.html"
    
class EmailEditSuccessView(TemplateView):
    template_name = "temp_messages/email_change_successful.html"
    