from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from datetime import datetime
from branches.models import Branch


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
    groups = models.ManyToManyField(Group, related_name="customuser_set")
    user_permissions = models.ManyToManyField(
        Permission, related_name="customuser_permissions"
    )
    def __str__(self):
        return self.username


class EmployeeUser(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    legajo = models.CharField(max_length=20)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="employees",
        null=True,
    )
    username = models.CharField(max_length=100, unique=True)  # Generado automáticamente
    password = models.CharField(max_length=100)  # Generado aleatoriamente



    groups = models.ManyToManyField(Group, related_name='employeeuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='employeeuser_permissions')

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.user.username})"
