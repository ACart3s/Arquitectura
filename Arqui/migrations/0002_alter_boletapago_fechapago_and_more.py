# Generated by Django 5.0.6 on 2024-11-13 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Arqui', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boletapago',
            name='fechaPago',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='deptohabitante',
            name='fechaTermino',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]