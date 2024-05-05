from allauth.account.forms import SignupForm
from django import forms


class CustomUserCreationForm(SignupForm):
    dni = forms.CharField(max_length=30, label="DNI")
    birthdate = forms.DateField(label="Fecha de Nacimiento")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

    def save(self, request):
        user = super(CustomUserCreationForm, self).save(request)
        user.dni = self.cleaned_data["dni"]
        user.birthdate = self.cleaned_data["birthdate"]
        user.save()
        return user


# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#
# class CustomUserCreationForm(UserCreationForm):
#
#    class Meta:
#        model = get_user_model()
#        fields = (
#            "username",
#            "email",
#        )
#
#
# class CustomUserChangeForm(UserChangeForm):
#
#    class Meta:
#        model = get_user_model()
#        fields = (
#            "username",
#            "email",
#        )
