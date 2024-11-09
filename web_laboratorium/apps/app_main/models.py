from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta

from web_laboratorium.apps.app_auth.models import UMSUser


def PeriodeField():
    return models.CharField(max_length=4,
    choices=[(str(i), str(i)) for i in range(datetime.now().year-3, datetime.now().year+3)],
    default=str(datetime.now().year))

def IPKField():
    return models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00),  
            MaxValueValidator(4.00),  
        ],
        default=3.00
    )

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
def NilaiField():
    return models.CharField(max_length=2, choices=NILAI_CHOICES, default='B')

def NumberNilaiField():
    return models.IntegerField(null=True, blank=True, max_length=3, validators=[MinValueValidator(0), MaxValueValidator(100)])
class Matkul(models.Model):
    nama_matkul = models.CharField(max_length=100)

class Praktikum(models.Model):
    praktikum_name = models.CharField(max_length=100)
    semester = models.PositiveSmallIntegerField(default=4, null=False)
    matkul = models.ForeignKey(Matkul, on_delete=models.DO_NOTHING, null=True)

    @property
    def practicum_name(self):
        return self.praktikum_name

    def __str__(self):
        return self.praktikum_name

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
    periode = PeriodeField()
    created_at = models.DateTimeField(default=datetime.now)
    def __str__(self):
        nim = self.user.email.split('@')[0]
        return f"{nim} {self.user.first_name} ({self.praktikum.praktikum_name} - {self.divisi})"
        # if self.asistensi:
        #     return f"{nim} {self.user.first_name} {self.praktikum.praktikum_name} {self.asistensi.asistensi_name}"

class Persyaratan(models.Model):
    lampiran = models.FileField(upload_to=settings.PERSYARATAN_URL)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    praktikum = models.ForeignKey(Praktikum, on_delete=models.DO_NOTHING, null=True)
    periode = PeriodeField()
    mulai_daftar = models.DateField(default=datetime.now().date())
    selesai_daftar = models.DateField(default=(datetime.now() + timedelta(days=21)).date())
    pengumuman = models.DateField(default=(datetime.now() + timedelta(days=60)).date())
    ipk = IPKField()
    nilai = NilaiField()
    active = models.BooleanField(default=True)

    @property
    def file(self):
        return self.lampiran

    def __str__(self):
        return f"{self.praktikum} {self.periode}"
    # {"-ACTIVE" if self.active else ""}

class Pendaftaran(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True, default=None)
    # PRAKTIKUM_CHOICES = (
    #     ('prokom', 'Pemrograman Komputer'),
    #     ('Statis', 'Statisika'),
    #     ('pti', 'Perancangan Teknik Industri'),
    # )
    # praktikum = models.ForeignKey(Praktikum, on_delete=models.CASCADE)
    persyaratan = models.ForeignKey(Persyaratan, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(UMSUser, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        (1, "Seleksi Pemberkasan"),
        (2, "Tes Microteaching"),
        (3, "Tes Pemahaman"),
        (4, "Wawancara Asisten"),
        (5, "Wawancara Dosen"),
        (6, "Diterima"),
        (-1, "Ditolak"),
    )
    nilai_tm = NumberNilaiField()
    nilai_tp = NumberNilaiField()
    nilai_wa = NumberNilaiField()
    nilai_wd = NumberNilaiField()

    catatan_wa = models.TextField(null=True, blank=True)
    catatan_wd = models.TextField(null=True, blank=True)

    selection_status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    ipk = IPKField()
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    nilai = NilaiField()

    @property
    def file(self):
        return self.berkas

    @property
    def status(self):
        return self.selection_status

    @property
    def praktikum(self):
        return self.persyaratan.praktikum

    @property
    def berkas_revision(self):
        total_unrevised = 0
        total_revised = 0
        for jenis in Berkas.jenis_choices:
            unrevised = 0
            revised = 0
            try:
                last_two = self.berkas_set.filter(jenis=jenis[0]).order_by("uploaded_at")
                try:
                    if last_two[1].komentar_set.exists():
                        unrevised = 1
                except:
                    pass
                try:
                    if last_two[0].komentar_set.exists():
                        unrevised = 1
                    else:
                        if unrevised > 0:
                            revised = 1
                            unrevised = 0
                except:
                    if unrevised > 0:
                        revised = 1
                        unrevised = 0
            except:
                pass
            total_unrevised += unrevised
            total_revised += revised
        return {"unrevised": total_unrevised, "revised": total_revised}

    def nilai_status(self,status=None):
        if status == None:
            status = self.selection_status
        if status == 2:
            return self.nilai_tm
        if status == 3:
            return self.nilai_tp
        if status == 4:
            return self.nilai_wa
        if status == 5:
            return self.nilai_wd
        return -1

    def catatan_status(self,status=None):
        if status == None:
            status = self.selection_status
        if status == 4:
            return self.catatan_wa
        if status == 5:
            return self.catatan_wd
        return -1

    def set_nilai_status(self, nilai, status=None):
        if status == None:
            status = self.selection_status
        if status == 2:
            self.nilai_tm = nilai
        if status == 3:
            self.nilai_tp = nilai
        if status == 4:
            self.nilai_wa = nilai
        if status == 5:
            self.nilai_wd = nilai
        self.save()
        return self.nilai_status(status)

    def set_catatan_status(self, catatan, status=None):
        if status == None:
            status = self.selection_status
        if status == 4:
            self.catatan_wa = catatan
        if status == 5:
            self.catatan_wd = catatan
        self.save()
        return self.catatan_status(status)

    def next_status(self):
        if self.selection_status == 6 or self.selection_status == -1:
            return None
        if self.nilai_status() == None: # kalau status skrg perlu nilai tapi balum diisi
            return None
        self.selection_status += 1
        self.save()
        return self.selection_status

    def __str__(self):
        return f"{self.praktikum.praktikum_name} {self.uploaded_at.year}"

class Berkas(models.Model):
    file = models.FileField(upload_to=settings.PENDAFTARAN_URL)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # edited_at = models.DateTimeField(null=True, blank=True, default=None)
    pendaftaran = models.ForeignKey(Pendaftaran, on_delete=models.CASCADE)
    jenis_choices = (
        ('st', 'Sertifikat TOL'),
        ('sp', 'Sertifikat Pendukung'),
        ('e2', 'Essay 2 Peminatan'),
        ('sp', 'Essay Pengembangan'),
        ('cv', 'Curriculum Vitae'),
        ('ml', 'Motivation Letter'),
        ('sl', 'Surat Lamaran'),
        ('tn', 'Transkrip Nilai'),
        ('pi', 'Pakta Integritas'),
        ('ff', 'Foto Formal'),
    )
    jenis = models.CharField(max_length=2, choices=jenis_choices)
    # catatan = models.TextField(null=True, blank=True)
    # catatan_at = models.DateTimeField(null=True, blank=True, default=None)

class Komentar(models.Model):
    berkas = models.ForeignKey(Berkas, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    user = models.ForeignKey(UMSUser, on_delete=models.CASCADE)
    # {"-ACTIVE" if self.active else ""}
