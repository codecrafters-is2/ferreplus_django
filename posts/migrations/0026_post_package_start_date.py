# Generated by Django 5.0.4 on 2024-06-17 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0025_package_priority_alter_package_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='package_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
