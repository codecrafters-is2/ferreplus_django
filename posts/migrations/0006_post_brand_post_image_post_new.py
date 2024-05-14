# Generated by Django 5.0.4 on 2024-05-04 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='brand',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to='productos'),
        ),
        migrations.AddField(
            model_name='post',
            name='new',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
