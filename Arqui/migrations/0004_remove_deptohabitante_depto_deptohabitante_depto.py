# Generated by Django 5.1.3 on 2024-11-06 13:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Arqui', '0003_alter_deptohabitante_fechainicio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deptohabitante',
            name='depto',
        ),
        migrations.AddField(
            model_name='deptohabitante',
            name='depto',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='Arqui.departamentos'),
            preserve_default=False,
        ),
    ]