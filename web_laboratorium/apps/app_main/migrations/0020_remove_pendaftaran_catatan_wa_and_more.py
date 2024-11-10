# Generated by Django 4.2.11 on 2024-11-10 07:30

import datetime
from django.db import migrations, models
import web_laboratorium.apps.app_main.models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0019_berkas_remove_pendaftaran_berkas_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pendaftaran',
            name='catatan_wa',
        ),
        migrations.RemoveField(
            model_name='pendaftaran',
            name='catatan_wd',
        ),
        migrations.AlterField(
            model_name='berkas',
            name='jenis',
            field=models.CharField(choices=[('st', 'Sertifikat TOL'), ('sp', 'Sertifikat Pendukung'), ('e2', 'Essay 2 Peminatan'), ('ep', 'Essay Pengembangan'), ('cv', 'Curriculum Vitae'), ('ml', 'Motivation Letter'), ('sl', 'Surat Lamaran'), ('tn', 'Transkrip Nilai'), ('pi', 'Pakta Integritas'), ('ff', 'Foto Formal')], max_length=2),
        ),
        migrations.AlterField(
            model_name='pendaftaran',
            name='nilai_tp',
            field=models.JSONField(blank=True, null=True, validators=[web_laboratorium.apps.app_main.models.validate_tes_pemahaman]),
        ),
        migrations.AlterField(
            model_name='pendaftaran',
            name='nilai_wa',
            field=models.JSONField(blank=True, null=True, validators=[web_laboratorium.apps.app_main.models.validate_wawancara]),
        ),
        migrations.AlterField(
            model_name='pendaftaran',
            name='nilai_wd',
            field=models.JSONField(blank=True, null=True, validators=[web_laboratorium.apps.app_main.models.validate_wawancara]),
        ),
        migrations.AlterField(
            model_name='persyaratan',
            name='mulai_daftar',
            field=models.DateField(default=datetime.date(2024, 11, 10)),
        ),
        migrations.AlterField(
            model_name='persyaratan',
            name='pengumuman',
            field=models.DateField(default=datetime.date(2025, 1, 9)),
        ),
        migrations.AlterField(
            model_name='persyaratan',
            name='selesai_daftar',
            field=models.DateField(default=datetime.date(2024, 12, 1)),
        ),
    ]
