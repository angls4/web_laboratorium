from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


class Matkul(models.Model):
    nama_matkul = models.CharField(max_length=100)

class Praktikum(models.Model):
    practicum_name = models.CharField(max_length=100)
    semester = models.PositiveSmallIntegerField(default=4, null=False)
    matkul = models.ForeignKey(Matkul, on_delete=models.DO_NOTHING, null=True)
    def __str__(self):
        return self.practicum_name

class Asisten(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    praktikum = models.ForeignKey(Praktikum, on_delete=models.DO_NOTHING, null=True)
    DIVISI_CHOICES = [
        ('Bendahara', 'Bendahara'),
        ('HRD', 'HRD'),
        ('K3', 'K3'),
        ('Koordinator', 'Koordinator'),
        ('Maintenance', 'Maintenance'),
        ('Multimedia', 'Multimedia'),
        ('RND', 'RND'),
        ('Sekretaris', 'Sekretaris'),
    ]
    divisi = models.CharField(max_length=100, choices=DIVISI_CHOICES, null=True)
    # periode = models.CharField(max_length=4, null=True)
    # PERIODE_CHOICES = [
    #     ('2020-2021', '2020-2021'),
    #     ('2021-2022', '2021-2022'),
    #     ('2022-2023', '2022-2023'),
    #     ('2023-2024', '2023-2024'),
    #     ('2024-2025', '2024-2025'),
    # ]
    periode = models.CharField(max_length=4,
    choices=[
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
    ],
    default=str(datetime.now().year))
    created_at = models.DateTimeField(default=datetime.now)
    def __str__(self):
        nim = self.user.email.split('@')[0]
        return f"{nim} {self.user.first_name} ({self.praktikum.practicum_name} - {self.divisi})"
        # if self.asistensi:
        #     return f"{nim} {self.user.first_name} {self.praktikum.practicum_name} {self.asistensi.asistensi_name}"

class Pendaftaran(models.Model):
    file = models.FileField(upload_to=settings.PENDAFTARAN_URL)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    PRAKTIKUM_CHOICES = (
        ('prokom', 'Pemrograman Komputer'),
        ('Statis', 'Statisika'),
        ('pti', 'Perancangan Teknik Industri'),
    )
    praktikum = models.ForeignKey(Praktikum, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        (1, "Seleksi Pemberkasan"),
        (2, "Lolos Seleksi Pemberkasan"),
        (3, "Tes Microteaching"),
        (4, "Lolos Microteaching"),
        (5, "Tes Pemahaman"),
        (6, "Lolos Pemahaman"),
        (7, "Wawancara Asisten"),
        (8, "Lolos Wawancara Asisten"),
        (9, "Wawancara Dosen"),
        (10, "Lolos Wawancara Dosen"),
        (11, "Diterima"),
        (-1, "Ditolak"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    ipk = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00),  
            MaxValueValidator(4.00),  
        ],
    )
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    NILAI_CHOICES = (
        ('A', 'A'),
        ('AB', 'AB'),
        ('B', 'B'),
        ('BC', 'BC'),
        ('C', 'C'),
        ('CD', 'CD'),
        ('D', 'D'),
        ('DE', 'DE'),
        ('E', 'E'),
    )
    nilai = models.CharField(max_length=2, choices=NILAI_CHOICES, default='A')

class Persyaratan(models.Model):
    file = models.FileField(upload_to=settings.PERSYARATAN_URL)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.file.name}{'-ACTIVE' if self.active else ''}"
