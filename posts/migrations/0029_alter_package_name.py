# Generated by Django 5.0.6 on 2024-06-26 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0028_alter_packagepurchase_package_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='name',
            field=models.CharField(choices=[('Ninguno', 'Ninguno'), ('Bronce', 'Bronce'), ('Plata', 'Plata'), ('Oro', 'Oro')], default='Ninguno', max_length=10, unique=True),
        ),
    ]
