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
    dni = models.IntegerField(
        unique=False,
        null=True,
        default=None,
    )
    birthdate = models.DateField(default=None, null=True)

