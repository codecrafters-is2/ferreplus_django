from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser
from datetime import datetime
from django.contrib.auth.models import Group


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

        password: str = cleaned_data.get("password1")
        password_repeat: str = cleaned_data.get("password2")
        if  password != password_repeat:
            self.add_error(
                "password1",
                ("Las contraseñas no coinciden"),
            )
        if not (any(caracter.isdigit() for caracter in password)):
            self.add_error(
                "password1",
                ("La contraseña debe incluir algún caracter numérico"),
            )
        if not (any(caracter.isalpha() for caracter in password)):
            self.add_error(
                "password1",
                ("La contraseña debe incluir alguna letra (a-z)"),
            )
        if  len(password) < 8:
            self.add_error(
                "password1",
                ("La contraseña debe tener al menos 8 caracteres"),
            )
        
        return self.cleaned_data

    def save(self, request):
        user = super(CustomUserCreationForm, self).save(request)
        user.dni = self.cleaned_data["dni"]
        user.birthdate = self.cleaned_data["birthdate"]
        user.save()
        grupo = Group.objects.get(name='client')
        user.groups.add(grupo)
        return user

