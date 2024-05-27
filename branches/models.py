from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class ActiveManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_active=True)
    #self.fields['branch'].queryset = Branch.active_objects.all() para levantar sólo las activas en cualquier lugar

class Branch(models.Model):
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    phone = PhoneNumberField(
        error_messages={'invalid': 'Por favor, introduce un número de teléfono válido.'},
        help_text='  Formato: +54 12345678'
        )
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()

    def delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.city} - {self.address}"
