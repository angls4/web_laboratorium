import re
from django import forms
from django.conf import settings

from .models import Berkas, Pendaftaran, Persyaratan, berkas_jenises
from datetime import date, datetime

class FormPersyaratan(forms.ModelForm):
    class Meta:
        model = Persyaratan
        fields = ["lampiran", "praktikum", "periode", "mulai_daftar", "selesai_daftar", "pengumuman"]
        widgets = {
            "lampiran": forms.ClearableFileInput(attrs={"id": "id_file", "accept": "image/*"}),
            "mulai_daftar": forms.DateInput(attrs={"type": "date"}),
            "selesai_daftar": forms.DateInput(attrs={"type": "date"}),
            "pengumuman": forms.DateInput(attrs={"type": "date"}),
        }
        required = ["lampiran", "praktikum", "periode", "mulai_daftar", "selesai_daftar", "pengumuman"]

    def __init__(self, *args, **kwargs):
        super(FormPersyaratan, self).__init__(*args, **kwargs)
        # self.fields['praktikum'].disabled = True
        # self.fields["periode"].disabled = False

    def clean_lampiran(self):
        file = self.cleaned_data.get("lampiran")
        if not file:
            return self.instance.lampiran
        return file

    def save(self, commit=True):
        persyaratan = super().save(commit=False)
        if self.files.get("lampiran"):
            persyaratan.lampiran.name = f"{persyaratan.praktikum}_{persyaratan.periode}"
            persyaratan.save(commit)
        return persyaratan

    # def save(self):
    #     persyaratan = Persyaratan()
    #     persyaratan.file_persyaratan = self.cleaned_data["file_persyaratan"]
    #     persyaratan.active = True
    #     current_active = Persyaratan.objects.filter(active=True).latest('uploaded_at')
    #     if current_active:
    #         current_active.active = False
    #         current_active.save()
    #     persyaratan.save()
    #     return persyaratan

class PendaftaranFileInput(forms.ClearableFileInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"].update(
            {
                "initial_text": "File saat ini",
                "input_text": "Ubah file",
            }
        )
        return context

    def format_value(self, value):
        if self.is_initial(value):
            print(value.__dict__["instance"].__dict__)
            return value
        return None
class UploadPendaftaran(forms.ModelForm):
    # berkas = forms.FileField(
    #     widget=PendaftaranFileInput(attrs={"id": "id_file", "accept": ".zip,.rar"}),
    #     help_text=".zip/.rar",
    #     label="File Praktikum",
    # )
    class Meta:
        model = Pendaftaran
        # fields = ["berkas", "persyaratan", "ipk", "nilai", "linkedin", "instagram","selection_status"]
        fields = ["persyaratan", "ipk", "nilai", "linkedin", "instagram","selection_status"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(UploadPendaftaran, self).__init__(*args, **kwargs)
        self.fields['ipk'].required = True
        self.fields['nilai'].required = True
        self.fields['linkedin'].required = True
        self.fields['instagram'].required = True
        self.fields['persyaratan'].label = "Daftar Untuk"

        if self.instance and self.instance.pk:
            self.fields['selection_status'].disabled = True
            self.fields["selection_status"].required = False
            self.fields['persyaratan'].disabled = True
            self.fields['persyaratan'].required = False
            # self.fields['praktikum'].disabled = True
            # self.fields['praktikum'].required = False
            # self.fields['berkas'].required = False
        else:
            for jenis in berkas_jenises:
                self.fields[f'berkas_{jenis[0]}'] = forms.FileField(
                    widget=PendaftaranFileInput(attrs={"name":f'berkas_{jenis[0]}' ,"id": f"id_{jenis[0]}", "accept": jenis[2]}),
                    help_text=jenis[2],
                    label=jenis[1] + (' (opsional)' if not jenis[3] else ''),
                    required=jenis[3],
                )
            self.fields.pop('selection_status')
            genap_ganjil_semester = 0 if datetime.now().month < 7 else 1
            self.fields['persyaratan'].queryset = self.fields['persyaratan'].queryset.filter(praktikum__semester__lte=3+genap_ganjil_semester, mulai_daftar__lte=datetime.now().date(), pengumuman__gte=datetime.now().date(), active=True)
            # self.fields['praktikum'].queryset = self.fields['praktikum'].queryset.filter(semester__lte=3+genap_ganjil_semester)

    # def cleanBerkases(self):
    #     for jenis in berkas_jenises:
    #         file = self.cleaned_data.get(f'berkas_{jenis[0]}')
    #         if not file:
    #             continue
    #         if not re.match(jenis[2], file.name):
    #             raise forms.ValidationError(
    #                 f"File {jenis[1]} harus berformat {jenis[2]}"
    #             )

    def clean(self):
        cleaned_data = super().clean()
        # self.cleanBerkases()
        persyaratan = cleaned_data.get("persyaratan")
        print(persyaratan)
        print(self.request.user)
        if self.request.user and persyaratan:
            if not self.instance.pk:
                print(cleaned_data.get("ipk"))
                print(cleaned_data.get("nilai"))
                # check mulai_daftar, selesai_daftar
                if not persyaratan.mulai_daftar <= datetime.now().date() <= persyaratan.selesai_daftar:
                    raise forms.ValidationError(
                        f"Praktikum ini tidak sedang dalam periode pendaftaran (mulai {persyaratan.mulai_daftar}, selesai {persyaratan.selesai_daftar})"
                    )
                if cleaned_data.get("ipk") < persyaratan.ipk:
                    raise forms.ValidationError(
                        f"IPK Anda tidak memenuhi syarat untuk praktikum ini (syarat {persyaratan.ipk})"
                    )
                if cleaned_data.get("nilai") > persyaratan.nilai:
                    raise forms.ValidationError(
                        f"Nilai Anda tidak memenuhi syarat untuk praktikum ini (syarat {persyaratan.nilai})"
                    )

                current_year = datetime.now().year
                genap_ganjil_semester = 0 if datetime.now().month < 7 else 1
                current_semester = (current_year - self.request.user.angkatan) * 2 + genap_ganjil_semester
                if current_semester != persyaratan.praktikum.semester:
                    raise forms.ValidationError(
                        f"Semester Anda tidak memenuhi syarat untuk praktikum yang dipilih (semester anda {current_semester}, hanya terbuka untuk semester {persyaratan.praktikum.semester})"
                    )
                if Pendaftaran.objects.filter(
                    user=self.request.user, persyaratan__praktikum=persyaratan.praktikum
                ).exists():
                    raise forms.ValidationError(
                        "User telah mendaftar untuk praktikum ini sebelumnya"
                    )
        else:
            raise forms.ValidationError("User atau praktikum tidak ditemukan")

        return cleaned_data
    def save(self, commit=True, edited=False):
        pendaftaran = super().save(commit=False)
        # if self.files.get("berkas"):
        #     current_year = datetime.now().strftime("%Y")
        #     pendaftaran.berkas.name = f"{self.request.user.nim}_{pendaftaran.praktikum}_{current_year}"
        # # .{pendaftaran.file.name.split('.')[-1]}
        pendaftaran.user = self.request.user
        if edited:
            pendaftaran.edited_at = datetime.now()
        if commit:
            pendaftaran.save()
        for jenis in berkas_jenises:
            file = self.cleaned_data.get(f'berkas_{jenis[0]}')
            if not file:
                continue
            pendaftaran.berkas_set.create(file=file, jenis=jenis[0])
        return pendaftaran


class UpdatePendaftaran(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())
    selection_status = forms.ChoiceField(choices=Pendaftaran.STATUS_CHOICES, required=False)

    # class Meta:
    #     model = Pendaftaran

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(self.fields)
        self.fields["selection_status"].label = ""
