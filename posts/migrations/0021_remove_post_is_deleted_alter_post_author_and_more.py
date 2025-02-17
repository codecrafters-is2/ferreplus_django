# Generated by Django 5.0.4 on 2024-05-27 16:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0006_branch_is_active'),
        ('posts', '0020_post_is_deleted'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_deleted',
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='post',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='branches.branch', verbose_name='Sucursal'),
        ),
        migrations.AlterField(
            model_name='post',
            name='brand',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('tools', 'Herramientas'), ('construction', 'Construcción'), ('general_hardware_store', 'Ferretería general'), ('electrical', 'Electricidad'), ('plumbing', 'Fontanería'), ('gardens', 'Jardin')], max_length=22, verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('available', 'Disponible'), ('reserved', 'Reservado'), ('completed', 'Finalizado'), ('paused', 'Pausado'), ('deleted', 'Eliminado')], default='available', max_length=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Titulo'),
        ),
    ]
