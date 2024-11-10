import json
from math import e
import re
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta
from jsonschema import validate, ValidationError

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

    def getDict(self):
        return {
            "nim": self.user.email.split("@")[0],
            "nama": self.user.first_name,
            "nama_praktikum": self.praktikum.praktikum_name,
            "id_praktikum": self.praktikum.id,
            "divisi": self.divisi,
            "periode": self.periode,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

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


tes_microteaching_schema = {
    "type": "object",
    "properties": {
        "nilai": {"type": "integer", "minimum": 1, "maximum": 100},
        "komentar": {"type": "string"},
    },
    "additionalProperties": False,
    "required": ["nilai", "komentar"],
}

tes_pemahaman_schema = {
    "type": "object",
    "properties": {
        "pm": {"type": "integer", "minimum": 1, "maximum": 100},
        "km": {"type": "integer", "minimum": 1, "maximum": 100},
        "mk": {"type": "integer", "minimum": 1, "maximum": 100},
        "kmp": {"type": "integer", "minimum": 1, "maximum": 100},
        "sp": {"type": "integer", "minimum": 1, "maximum": 100},
        "komentar": {"type": "string"},
    },
    "additionalProperties": False,
    "required": ["pm", "km", "mk", "kmp", "sp", "komentar"],
}

wawancara_schema = {
    "type": "object",
    "properties": {
        "pd": {"type": "integer", "minimum": 1, "maximum": 5},
        "rrd": {"type": "integer", "minimum": 1, "maximum": 5},
        "mdb": {"type": "integer", "minimum": 1, "maximum": 5},
        "komentar": {"type": "string"}
    },
    "additionalProperties": False,
    "required": ["pd", "rrd", "mdb", "komentar"]
}

def validate_json(value, schema):
    try:
        validate(instance=value, schema=schema)
        return True
    except ValidationError as e:
        raise ValueError(f"Invalid JSON data: {e.message}")

def validate_tes_microteaching(value):
    validate_json(value, tes_microteaching_schema)

def validate_tes_pemahaman(value):
    validate_json(value, tes_pemahaman_schema)

def validate_wawancara(value):
    validate_json(value, wawancara_schema)


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
    # Tes Microteaching
    nilai_tm = models.JSONField(null=True, blank=True, validators=[validate_tes_microteaching])
    # Tes Pemahaman
    nilai_tp = models.JSONField(null=True, blank=True, validators=[validate_tes_pemahaman])
    # Wawancara Asisten
    nilai_wa = models.JSONField(null=True, blank=True, validators=[validate_wawancara])
    # Wawancara Dosen
    nilai_wd = models.JSONField(null=True, blank=True, validators=[validate_wawancara])

    # catatan_wa = models.TextField(null=True, blank=True)
    # catatan_wd = models.TextField(null=True, blank=True)

    selection_status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    ipk = IPKField()
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    nilai = NilaiField()

    def getDict(self):
        return {
            "id": self.id,
            "nim": self.user.nim,
            "nama": self.user.first_name,
            "linkedin": self.linkedin,
            "instagram": self.instagram,
            "uploaded_at_int": int(self.uploaded_at.timestamp()),
            "tahun": self.uploaded_at.year,
            "uploaded_at": self.uploaded_at.strftime("%Y-%m-%d"),
            "edited_at": (
                self.edited_at.strftime("%Y-%m-%d")
                if self.edited_at
                else "-"
            ),
            "ipk": str(self.ipk),
            "nilai_id": self.nilai,
            "nilai": self.get_nilai_display(),
            "status_id": self.status,
            "status": self.get_selection_status_display(),
            "berkas_revision": self.berkas_revision,
            "nilai_tp": self.nilai_tp,
            "nilai_tm": self.nilai_tm,
            "nilai_wa": self.nilai_wa,
            "nilai_wd": self.nilai_wd,
        }

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
            revision = self.jenis_revision(jenis[0])
            if revision == 1:
                total_unrevised += 1
            elif revision == 2:
                total_revised += 1
        return {"unrevised": total_unrevised, "revised": total_revised}

    def jenis_revision(self, jenis):
        revision = 0
        print(jenis )
        try:
            rows = self.berkas_set.filter(jenis=jenis).all().order_by("uploaded_at").reverse()
            i = 0
            inc = 1
            while i < len(rows):
                print(rows[i].__dict__, rows[i].komentar_set.exists())
                if rows[i].komentar_set.exists():
                    revision = 1
                    inc = -1
                elif not rows[i].komentar_set.exists() and revision == 1:
                    revision = 2
                    break
                i += inc
            # print(revised, unrevised)

            # try:
            #     if last_two[1].komentar_set.exists():
            #         unrevised = 1
            # except:
            #     pass
            # try:
            #     revisi = self.berkas_set.filter(jenis=jenis).all().order_by("uploaded_at").reverse().filter(komentar_set__isnull=True)[0]
            #     if lrevisi:
            #         unrevised = 1
            #     else:
            #         if unrevised > 0:
            #             revised = 1
            #             unrevised = 0
            # except:
            #     if unrevised > 0:
            #         revised = 1
            #         unrevised = 0
            # print(revised, unrevised)
        except Exception as e:
            print(e)
        # revision = 2 if revised == 1 else 1 if unrevised == 1 else 0
        print("revision",revision)
        return revision

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

    def clean_nilai_tm(self):
        validate_tes_microteaching(self.nilai_tm)
    def clean_nilai_tp(self):
        validate_tes_pemahaman(self.nilai_tp)
    def clean_nilai_wa(self):
        validate_wawancara(self.nilai_wa)
    def clean_nilai_wd(self):
        validate_wawancara(self.nilai_wd)

    def set_nilai_status(self, nilai, status=None):
        if status == None:
            status = self.selection_status
        try:
            if status == 2:
                # print(validate_tes_microteaching(nilai))
                self.nilai_tm = nilai
                self.clean_nilai_tm()
            if status == 3:
                self.nilai_tp = nilai
                self.clean_nilai_tp()
            if status == 4:
                self.nilai_wa = nilai
                self.clean_nilai_wa()
            if status == 5:
                self.nilai_wd = nilai
                self.clean_nilai_wd()
            # self.full_clean()
            self.save()
        except Exception as e:
            print(e)
            raise ValueError(f"Invalid JSON data: {e}")
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
        if self.selection_status == 1 and self.berkas_revision["unrevised"] > 0:
            return None
        self.selection_status += 1
        self.save()
        return self.selection_status

    def __str__(self):
        return f"{self.praktikum.praktikum_name} {self.uploaded_at.year}"


berkas_jenises = (
    ("st", "Sertifikat TOL", ".pdf", True),
    ("sp", "Sertifikat Pendukung", ".pdf", False),
    ("e2", "Essay 2 Peminatan", ".pdf", True),
    ("ep", "Essay Pengembangan", ".pdf", True),
    ("cv", "Curriculum Vitae", ".pdf", True),
    ("ml", "Motivation Letter", ".pdf", True),
    ("sl", "Surat Lamaran", ".pdf", True),
    ("tn", "Transkrip Nilai", ".pdf", True),
    ("pi", "Pakta Integritas", ".pdf", True),
    ("ff", "Foto Formal", ".jpg,.png,.jpeg", True),
)
class Berkas(models.Model):
    file = models.FileField(upload_to=settings.PENDAFTARAN_URL)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # edited_at = models.DateTimeField(null=True, blank=True, default=None)
    pendaftaran = models.ForeignKey(Pendaftaran, on_delete=models.CASCADE)
    jenis_choices = [(jenis[0], jenis[1]) for jenis in berkas_jenises]
    jenis = models.CharField(max_length=2, choices=jenis_choices)

    def save(self, *args, **kwargs):
        current_year = datetime.now().year
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.file.name = f"{self.pendaftaran.user.nim}_{self.pendaftaran.praktikum.praktikum_name}_{current_year}_{timestamp}{self.file.name[self.file.name.rfind('.'):]}"
        super().save(*args, **kwargs)
    # def asisten(self):
    # return self.file.name
    # catatan = models.TextField(null=True, blank=True)
    # catatan_at = models.DateTimeField(null=True, blank=True, default=None)

class Komentar(models.Model):
    berkas = models.ForeignKey(Berkas, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    user = models.ForeignKey(UMSUser, on_delete=models.CASCADE)
    # {"-ACTIVE" if self.active else ""}
