from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser


class CustomUserCreationForm(SignupForm):
   pass

    # dni = forms.CharField(
    #    label="DNI",
    #    widget=forms.TextInput(
    #        attrs={
    #            "placeholder": ("DNI"),
    #            "type": "number",
    #        }
    #    ),
    # )
    # birthdate = forms.DateField(
    #    label="Fecha de Nacimiento",
    #    widget=forms.DateInput(
    #        attrs={
    #            "placeholder": ("Fecha de Nacimiento"),
    #            "type": "date",
    #        }
    #    ),
    # )

    # def __init__(self, *args, **kwargs):
    #    super(CustomUserCreationForm, self).__init__(*args, **kwargs)

    # def clean(self):
    #    cleaned_data = super(SignupForm, self).clean()
#
#    # current_year = datetime.now().year
#    # birthdate_value = cleaned_data.get("birthdate")
#    # if (current_year - birthdate_value.year) < 18:
#    #    self.add_error(
#    #        "birthdate",
#    #        ("Para registrarte como usuario debes ser mayoy de 18 años!"),
#    #    )
#    # dni_value = cleaned_data.get("dni")
#    # if User.objects.filter(dni=dni_value).exists():
#    #    self.add_error(
#    #        "dni",
#    #        ("El DNI ingresado ya está registrado en el sistema"),
#    #    )
#    return self.cleaned_data

# def save(self, request):
#    user = super(CustomUserCreationForm, self).save(request)
#    #print("USEEEEER -----> ", user)
#    #user.dni = self.cleaned_data["dni"]
#    print("VALOR DE DNI RECIBIDOOO --> ", self.cleaned_data["dni"])
#    #user.birthdate = self.cleaned_data["birthdate"]
# user.save()
# return user
