# Generated by Django 4.2.11 on 2024-11-09 05:26

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_main', '0018_rename_file_pendaftaran_berkas_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Berkas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/pendaftaran/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('jenis', models.CharField(choices=[('st', 'Sertifikat TOL'), ('sp', 'Sertifikat Pendukung'), ('e2', 'Essay 2 Peminatan'), ('sp', 'Essay Pengembangan'), ('cv', 'Curriculum Vitae'), ('ml', 'Motivation Letter'), ('sl', 'Surat Lamaran'), ('tn', 'Transkrip Nilai'), ('pi', 'Pakta Integritas'), ('ff', 'Foto Formal')], max_length=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='pendaftaran',
            name='berkas',
        ),
        migrations.AddField(
            model_name='pendaftaran',
            name='catatan_wa',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pendaftaran',
            name='catatan_wd',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pendaftaran',
            name='nilai_tm',
            field=models.IntegerField(blank=True, max_length=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='pendaftaran',
            name='nilai_tp',
            field=models.IntegerField(blank=True, max_length=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='pendaftaran',
            name='nilai_wa',
            field=models.IntegerField(blank=True, max_length=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='pendaftaran',
            name='nilai_wd',
            field=models.IntegerField(blank=True, max_length=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='pendaftaran',
            name='selection_status',
            field=models.IntegerField(choices=[(1, 'Seleksi Pemberkasan'), (2, 'Tes Microteaching'), (3, 'Tes Pemahaman'), (4, 'Wawancara Asisten'), (5, 'Wawancara Dosen'), (6, 'Diterima'), (-1, 'Ditolak')], default=1),
        ),
        migrations.AlterField(
            model_name='persyaratan',
            name='mulai_daftar',
            field=models.DateField(default=datetime.date(2024, 11, 9)),
        ),
        migrations.AlterField(
            model_name='persyaratan',
            name='pengumuman',
            field=models.DateField(default=datetime.date(2025, 1, 8)),
        ),
        migrations.AlterField(
            model_name='persyaratan',
            name='selesai_daftar',
            field=models.DateField(default=datetime.date(2024, 11, 30)),
        ),
        migrations.CreateModel(
            name='Komentar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('berkas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_main.berkas')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='berkas',
            name='pendaftaran',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_main.pendaftaran'),
        ),
    ]
