# Generated by Django 4.2.11 on 2024-10-19 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0002_umsuser_angkatan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='umsuser',
            name='instagram',
        ),
        migrations.RemoveField(
            model_name='umsuser',
            name='linkedin',
        ),
    ]
