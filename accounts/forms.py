from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser
from datetime import datetime
from datetime import date
from django.contrib.auth import password_validation
from allauth.account.forms import PasswordField
from allauth.account.adapter import get_adapter
from ferreplus import settings
from django.contrib.auth import get_user_model
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

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["password1"] = PasswordField(
            label=("Password"),
            autocomplete="new-password",
            help_text=password_validation.password_validators_help_text_html(),
        )
        if settings.SIGNUP_PASSWORD_ENTER_TWICE:
            self.fields["password2"] = PasswordField(
                label=("Password (again)"), autocomplete="new-password"
            )

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()

        # Clean DNI
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

        # Clean birthdate
        actual_year = datetime.now().year
        birthdate_value = cleaned_data.get("birthdate")
        if (actual_year - birthdate_value.year) < 18:
            self.add_error(
               "birthdate",
               ("Para registrarte como usuario debes ser mayor de 18 años."),
           )

        if birthdate_value.year > actual_year:
            self.add_error(
                "birthdate",
                (
                    "¡La fecha de nacimiento ingresada es inválida!"
                ),
            )
        if birthdate_value.year <= 1904:
            self.add_error(
                "birthdate",
                ("¡La fecha de nacimiento ingresada es inválida!"),
            )

        # Clean Password
        User = get_user_model()
        dummy_user = User()

        password = self.cleaned_data.get("password1")
        if password:
            try:
                get_adapter().clean_password(password, user=dummy_user)
            except forms.ValidationError as e:
                self.add_error("password1", e)

        if (
            settings.SIGNUP_PASSWORD_ENTER_TWICE
            and "password1" in self.cleaned_data
            and "password2" in self.cleaned_data
        ):
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                self.add_error(
                    "password2",
                    ("Las contraseñas ingresadas no coinciden."),
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
        user.password1 = self.cleaned_data["password1"]
        user.password2 = self.cleaned_data["password2"]
        user.save()
        grupo = Group.objects.get(name='client')
        user.groups.add(grupo)
        return user
