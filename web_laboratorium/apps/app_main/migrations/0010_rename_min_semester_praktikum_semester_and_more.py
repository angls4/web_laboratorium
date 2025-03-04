# Generated by Django 4.2.11 on 2024-10-21 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0009_persyaratan'),
    ]

    operations = [
        migrations.RenameField(
            model_name='praktikum',
            old_name='min_semester',
            new_name='semester',
        ),
        migrations.AddField(
            model_name='praktikum',
            name='matkul',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app_main.matkul'),
        ),
        migrations.AlterField(
            model_name='asisten',
            name='divisi',
            field=models.CharField(choices=[('Bendahara', 'Bendahara'), ('HRD', 'HRD'), ('K3', 'K3'), ('Koordinator', 'Koordinator'), ('Maintenance', 'Maintenance'), ('Multimedia', 'Multimedia'), ('RND', 'RND'), ('Sekretaris', 'Sekretaris')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pendaftaran',
            name='nilai',
            field=models.CharField(choices=[('A', 'A'), ('AB', 'AB'), ('B', 'B'), ('BC', 'BC'), ('C', 'C'), ('CD', 'CD'), ('D', 'D'), ('DE', 'DE'), ('E', 'E')], default='A', max_length=2),
        ),
        migrations.DeleteModel(
            name='PraktikumMatkul',
        ),
    ]
