# Generated by Django 5.0.4 on 2024-05-12 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0003_alter_branch_phone'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='branch',
            unique_together={('address', 'city', 'postal_code')},
        ),
    ]
