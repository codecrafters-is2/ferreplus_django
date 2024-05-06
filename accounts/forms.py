from allauth.account.forms import SignupForm
from django import forms
from datetime import datetime


class CustomUserCreationForm(SignupForm):
    dni = forms.IntegerField(
        label="DNI",
        widget=forms.TextInput(
            attrs={
                "placeholder": ("DNI"),
                "type": "number",
            }
        ),
    )
    birthdate = forms.DateField(
        label="Fecha de Nacimiento",
        widget=forms.TextInput(
            attrs={
                "placeholder": ("Fecha de Nacimiento"),
                "type": "date",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        current_year = datetime.now().year
        birthdate_value = cleaned_data.get("birthdate")
        if (current_year - birthdate_value.year) < 18:
            self.add_error(
                "birthdate",
                ("Para registrarte como usuario debes ser mayoy de 18 años!"),
            )
        return self.cleaned_data

    def save(self, request):
        user = super(CustomUserCreationForm, self).save(request)
        user.dni = self.cleaned_data["dni"]
        user.birthdate = self.cleaned_data["birthdate"]
        user.save()
        return user


#    def clean(self):
#        cleaned_data = super(BaseSignupForm, self).clean()
#        if app_settings.SIGNUP_EMAIL_ENTER_TWICE:
#            email = cleaned_data.get("email")
#            email2 = cleaned_data.get("email2")
#            if (email and email2) and email != email2:
#                self.add_error("email2", _("You must type the same email each time."))
#        return cleaned_data


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
