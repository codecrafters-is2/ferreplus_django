# Generated by Django 5.0.4 on 2024-05-03 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='related_posts',
            field=models.ManyToManyField(blank=True, editable=False, related_name='related_by', to='posts.post'),
        ),
    ]
