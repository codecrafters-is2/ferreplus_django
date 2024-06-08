# Generated by Django 5.0.4 on 2024-05-25 18:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_question_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='related_posts',
        ),
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(150)]),
        ),
    ]
