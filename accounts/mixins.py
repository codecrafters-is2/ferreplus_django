from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class AdminRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="admi").exists():
            return super().dispatch(request, *args, **kwargs)
        return redirect('home')
