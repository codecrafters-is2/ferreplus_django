from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Branch(models.Model):
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    phone = PhoneNumberField(
        error_messages={'invalid': 'Por favor, introduce un número de teléfono válido.'},
        help_text='  Formato: +54 12345678'
        )


    def __str__(self):
        return self.city