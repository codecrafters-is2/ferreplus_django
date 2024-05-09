from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime


def validate_age(value):
    actual_year = datetime.now().year
    if (actual_year - value.year) < 18:
        raise ValidationError(
            ("Para registrarte como usuario debes ser mayoy de 18 años!"),
            params={"value": value},
        )


class CustomUser(AbstractUser):
    pass

   ## dni = models.IntegerField(
   ##     unique=False, #DESPUES HAY QUE SETEARLO EN TRUE
   ##     validators=[
   ##         MinValueValidator(10000000, message="¡Número de DNI invalido!"),
   ##         MaxValueValidator(99999999, message="¡Número de DNI invalido!"),
   ##     ],
   ##     error_messages={
   ##         "unique": ("El DNI ingresado ya se encuentra registrado en el sistema"),
   ##     },
   ##     
   ##     null=True
   ## )
    # birthdate = models.DateField(validators=[validate_age], default=None)

