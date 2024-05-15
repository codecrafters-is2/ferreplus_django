#from django.contrib.auth.views import PasswordChangeView
#from django.shortcuts import redirect
#from django.urls import reverse_lazy



#class ClientPasswordChangeView(ClientRequiredMixin, PasswordChangeView):
#    success_url = reverse_lazy('password_change_done')

#class CustomPasswordChangeView(ClientRequiredMixin, PasswordChangeView):
#    success_url = reverse_lazy('password_change_done')
    
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views import View
from accounts.mixins import ClientRequiredMixin
from allauth.account.views import EmailView

class ChangePasswordView(ClientRequiredMixin,View):
    template_name = 'password_change.html'

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante para mantener al usuario conectado
            messages.success(request, '¡Tu contraseña se actualizó correctamente!')
            password_success_message = '¡Tu contraseña se actualizó correctamente!'
            return redirect('home')
        
        # Si el formulario no es válido, conservamos los mensajes por defecto de Django
        return render(request, self.template_name, {'form': form, 'password_success_message': None})


class EditProfileView(EmailView):
    success_url = "profile_edit_success"
