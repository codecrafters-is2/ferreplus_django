# Generated by Django 5.0.4 on 2024-06-04 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_homecarouselbanner_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homecarouselbanner',
            name='title_position',
            field=models.CharField(default='right', max_length=20),
        ),
    ]
