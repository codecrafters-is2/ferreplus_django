from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser
from .models import EmployeeUser
from branches.models import Branch
from datetime import datetime
from datetime import date
from django.contrib.auth import password_validation
from allauth.account.forms import PasswordField
from allauth.account.adapter import get_adapter
from ferreplus import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import secrets
import string


def generate_password(longitud=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(characters) for i in range(longitud))
    return password


class EmployeeUserCreationForm(forms.ModelForm):
    class Meta:
        model = EmployeeUser
        fields = [
            "nombre",
            "apellido",
            "legajo",
            "branch",
            "email",
        ]  # Campos que va a completar el usuario
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Nombre: "}),
            "apellido": forms.TextInput(attrs={"placeholder": "Apellido: "}),
            "legajo": forms.TextInput(attrs={"placeholder": "Legajo: "}),
            "email": forms.TextInput(attrs={"placeholder": "Email: "}),
        }
        field_classes = {
            "nombre": forms.CharField,
            "apellido": forms.CharField,
            "legajo": forms.CharField,
            "email": forms.CharField,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["branch"].queryset = Branch.objects.filter(is_active=True)
        self.fields["nombre"].label = "Nombre"
        self.fields["apellido"].label = "Apellido"
        self.fields["legajo"].label = "Legajo"
        self.fields["branch"].queryset = Branch.active_objects.all()
        self.fields["branch"].label = "Asignar Sucursal"
        self.fields["email"].label = "Email"

    def clean(self):
        cleaned_data = super().clean()

        # Clean Legajo
        legajo_value = cleaned_data.get("legajo")
        if EmployeeUser.objects.filter(legajo=legajo_value).exists():
            self.add_error(
                "legajo",
                ("El legajo ingresado ya está registrado en el sistema"),
            )

        # Clean email
        email_value = cleaned_data.get("email")
        if (
            EmployeeUser.objects.filter(email=email_value).exists()
            or CustomUser.objects.filter(email=email_value).exists()
        ):
            self.add_error(
                "email",
                ("El email ingresado ya está registrado en el sistema"),
            )
        if "@" not in email_value:
            self.add_error(
                "email",
                ("¡Email inválido!"),
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.username = instance.legajo
        instance.password = generate_password()  # Generar password aleatorio

        if commit:
            instance.save()
        # creación de usuario Empleado
        user = CustomUser.objects.create_user(
            instance.username, instance.email, instance.password
        )
        user.save()
        grupo = Group.objects.get(name="employee")
        user.groups.add(grupo)

        return instance


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
                ("¡La fecha de nacimiento ingresada es inválida!"),
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

        return self.cleaned_data

    def save(self, request):
        user = super(CustomUserCreationForm, self).save(request)
        user.dni = self.cleaned_data["dni"]
        user.birthdate = self.cleaned_data["birthdate"]
        user.password1 = self.cleaned_data["password1"]
        user.password2 = self.cleaned_data["password2"]
        user.save()
        grupo = Group.objects.get(name="client")
        user.groups.add(grupo)
        return user
