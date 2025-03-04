# Generated by Django 4.2.11 on 2024-10-08 03:12

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Matkul',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_matkul', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Praktikum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('praktikum_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PraktikumMatkul',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_matkul', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_main.matkul')),
                ('id_praktikum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_main.praktikum')),
            ],
        ),
        migrations.CreateModel(
            name='Pendaftaran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/pendaftaran/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('praktikum', models.CharField(choices=[('prokom', 'Pemrograman Komputer'), ('Statis', 'Statisika'), ('pti', 'Perancangan Teknik Industri')], max_length=100)),
                ('status', models.CharField(choices=[('pemberkasan', 'Seleksi Pemberkasan'), ('tes', 'Lolos Tes'), ('w_asisten', 'Lolos Wawancara Asisten'), ('w_dosen', 'Lolos Wawancara Dosen'), ('diterima', 'Diterima'), ('ditolak', 'Ditolak')], default='diproses', max_length=100)),
                ('ipk', models.DecimalField(decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(4.0)])),
                ('nilai', models.DecimalField(decimal_places=0, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
