# Generated by Django 4.2.11 on 2024-10-31 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0005_remove_umsuser_is_active_remove_umsuser_semester'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='umsuser',
            name='is_staff',
        ),
    ]
