# Generated by Django 4.2.11 on 2024-10-19 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='umsuser',
            name='angkatan',
            field=models.PositiveIntegerField(choices=[(2020, '2020'), (2021, '2021'), (2022, '2022'), (2023, '2023'), (2024, '2024'), (2025, '2025')], default=2024),
        ),
    ]
