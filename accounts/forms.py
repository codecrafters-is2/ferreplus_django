from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser
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
       widget=forms.DateInput(
           attrs={
               "placeholder": ("Fecha de Nacimiento"),
               "type": "date",
           }
       ),
    )

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        dni_value = cleaned_data.get("dni")
        if CustomUser.objects.filter(dni=dni_value).exists():
            self.add_error(
                "dni",
                ("El DNI ingresado ya está registrado en el sistema"),
            )
        if (dni_value < 11111111) or (dni_value > 99999999):
            self.add_error(
                "dni",
                ("¡Número de DNI inválido!"),
            )

        actual_year = datetime.now().year
        birthdate_value = cleaned_data.get("birthdate")
        if (actual_year - birthdate_value.year) < 18:
           self.add_error(
               "birthdate",
               ("Para registrarte como usuario debes ser mayor de 18 años!"),
           )

        return self.cleaned_data

    def save(self, request):
        user = super(CustomUserCreationForm, self).save(request)
        user.dni = self.cleaned_data["dni"]
        user.birthdate = self.cleaned_data["birthdate"]
        user.save()
        return user

