# Generated by Django 5.0.4 on 2024-05-10 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_customuser_birthdate_alter_customuser_dni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birthdate',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='dni',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
