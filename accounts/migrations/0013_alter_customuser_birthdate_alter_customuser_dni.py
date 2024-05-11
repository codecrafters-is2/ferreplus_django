# Generated by Django 5.0.4 on 2024-05-10 11:23

import accounts.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_customuser_birthdate_alter_customuser_dni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birthdate',
            field=models.DateField(default=None, null=True, validators=[accounts.models.validate_age]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='dni',
            field=models.IntegerField(default=None, error_messages={'unique': 'El DNI ingresado ya se encuentra registrado en el sistema'}, null=True, unique=True, validators=[django.core.validators.MinValueValidator(10000000, message='¡Número de DNI invalido!'), django.core.validators.MaxValueValidator(99999999, message='¡Número de DNI invalido!')]),
        ),
    ]
