import os
from django import forms
from django.conf import settings
from .models import Pendaftaran, Persyaratan
from django.core.files.base import ContentFile
from datetime import datetime


class UploadPersyaratan(forms.ModelForm):
    class Meta:
        model = Persyaratan
        fields = ["file"]
        widgets = {
            "file": forms.ClearableFileInput(attrs={"id": "id_file", "accept": "image/*"})
        }

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


class UploadPendaftaran(forms.ModelForm):
    class Meta:
        model = Pendaftaran
        fields = ["file", "praktikum", "ipk", "nilai", "linkedin", "instagram"]
        widgets = {
            'file': forms.ClearableFileInput(attrs={'id': 'id_file', 'accept': '.zip,.rar'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(UploadPendaftaran, self).__init__(*args, **kwargs)
        self.fields['linkedin'].required = True
        self.fields['instagram'].required = True
        genap_ganjil_semester = 0 if datetime.now().month < 7 else 1
        self.fields['praktikum'].queryset = self.fields['praktikum'].queryset.filter(semester__lte=3+genap_ganjil_semester)

    def clean(self):
        cleaned_data = super().clean()
        praktikum = cleaned_data.get("praktikum")

        if self.request.user and praktikum:
            current_year = datetime.now().year
            genap_ganjil_semester = 0 if datetime.now().month < 7 else 1
            current_semester = (current_year - self.request.user.angkatan) * 2 + genap_ganjil_semester
            if current_semester != praktikum.semester:
                raise forms.ValidationError(
                    f"Semester Anda tidak memenuhi syarat untuk praktikum yang dipilih (semester anda {current_semester}, hanya terbuka untuk semester {praktikum.semester})"
                )
            if Pendaftaran.objects.filter(
                user=self.request.user, praktikum=praktikum
            ).exists():
                raise forms.ValidationError(
                    "User telah mendaftar untuk praktikum ini sebelumnya"
                )

        return cleaned_data


class UpdatePendaftaran(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())
    status = forms.ChoiceField(choices=Pendaftaran.STATUS_CHOICES, required=False)

    # class Meta:
    #     model = Pendaftaran

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(self.fields)
        self.fields["status"].label = ""
