
#from django.contrib import messages
#from django.contrib.auth.views import PasswordChangeView
#from django.urls import reverse_lazy

#class MyPasswordChangeView(PasswordChangeView):
#    template_name = "password_change.html"
#    success_url = reverse_lazy('password_change_done')  # Redirecciona aquí después del cambio de contraseña
#    #success_url = '/accounts/password/change/successful/'
#    def form_valid(self, form):
#        response = super().form_valid(form)
#        messages.success(self.request, '¡Contraseña cambiada con éxito!')
#        return response
