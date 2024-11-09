import datetime
from operator import ne
from django.http import HttpResponseForbidden, HttpResponseNotFound, JsonResponse

from web_laboratorium.apps.app_main.models import Berkas, Pendaftaran
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import render_to_string

@login_required
def dashboard_pdf(request):
    tahun_filter = request.GET.get("tahun") or ""
    nilai_filter = request.GET.get("nilai") or ""
    status_filter = request.GET.get("status") or ""
    sort_by = request.GET.get("sort_by", "uploaded_at") or "uploaded_at"
    order = request.GET.get("order", "asc") or "asc"
    if sort_by == "nama":
        sort_by = "user__first_name"
    if sort_by == "nim":
        sort_by = "user__email"
    reversed_columns = ["user__first_name", "user__email", "nilai"]
    if sort_by in reversed_columns:
        order = "desc" if order == "asc" else "asc"
    sort_by = f"-{sort_by}" if order == "desc" else sort_by

    if request.user.asisten:
        filter_kwargs = {}
        if tahun_filter:
            filter_kwargs["uploaded_at__year"] = int(tahun_filter)
        if nilai_filter:
            filter_kwargs["nilai"] = nilai_filter
        if status_filter:
            filter_kwargs["selection_status"] = int(status_filter)
        if not request.user.is_superuser:
            filter_kwargs["praktikum"] = request.user.asisten.praktikum
        pendaftarans = Pendaftaran.objects.filter(**filter_kwargs).order_by(sort_by)
    else:
        pendaftarans = Pendaftaran.objects.filter(user=request.user)

    rows = pendaftarans

    pdf_context = {
        "user": request.user,
        # "debug": True,
        "rows": rows,
        "tahun_filter": tahun_filter,
        "nilai_filter": nilai_filter,
        "status_filter": (
            dict(Pendaftaran.STATUS_CHOICES)[int(status_filter)]
            if status_filter
            else ""
        ),
        "date": datetime.datetime.now().strftime("%d %B %Y %H:%M"),
    }

    html_string = render_to_string("dashboard_pdf.html", pdf_context)
    return JsonResponse({"html_string": html_string})


def next_status(request):
    if request.method == "POST":
        id = request.POST.get("id")
        pendaftaran = Pendaftaran.objects.get(id=id)
        new_status = pendaftaran.next_status()
        status = 200 if new_status else 400
        return JsonResponse({"status": status, "next_status": new_status})
    return JsonResponse({"status": -1})

def set_nilai(request):
    if request.method == "POST":
        id = request.POST.get("id")
        nilai = request.POST.get("nilai")
        status = request.POST.get("status")
        pendaftaran = Pendaftaran.objects.get(id=id)
        new_nilai = pendaftaran.set_nilai_status(nilai, status)
        return JsonResponse({"status": 200, "nilai": new_nilai})
    return JsonResponse({"status": -1})

def set_catatan(request):
    if request.method == "POST":
        id = request.POST.get("id")
        catatan = request.POST.get("catatan")
        status = request.POST.get("status")
        pendaftaran = Pendaftaran.objects.get(id=id)
        new_catatan = pendaftaran.set_catatan_status(catatan, status)
        return JsonResponse({"status": 200, "catatan": new_catatan})
    return JsonResponse({"status": -1})

def delete_pendaftaran(request):
    id = request.POST.get("id")
    try:
        pendaftaran = Pendaftaran.objects.get(pk=id)
        if pendaftaran.user != request.user and not request.user.koordinator:
            return HttpResponseForbidden("Bukan pendaftar")
        pendaftaran.delete()
        return JsonResponse({"status": 200})
    except Pendaftaran.DoesNotExist:
        return HttpResponseNotFound("Pendaftaran tidak ada")

def flat_berkas(berkas):
    return {
        "id": berkas.id,
        "file": berkas.file.url,
        "komentars": [
            {
                "user": komentar.user.first_name,
                "content": komentar.content,
                "created_at": komentar.created_at,
            }
            for komentar in berkas.komentar_set.all()
        ],
    }

def get_berkasesList(request):
    id = request.GET.get("id")
    try:
        pendaftaran = Pendaftaran.objects.get(pk=id)
        if pendaftaran.user != request.user and not request.user.asisten:
            return HttpResponseForbidden("Bukan pendaftar")
        # berkases = pendaftaran.berkas_set.all()
        berkasesList = []
        for jenis_value,jenis_label in Berkas.jenis_choices:
            item = {
                "label": jenis_label,
                "berkases": []
            }
            try:
                berkases = pendaftaran.berkas_set.filter(jenis=jenis_value).order_by("uploaded_at")
                item["berkases"] = [
                    flat_berkas(b)
                    for b in berkases
                ]
            except Berkas.DoesNotExist:
                pass
            berkasesList.append(item)
        return JsonResponse({"status": 200, "berkasesList": berkasesList})
    except Pendaftaran.DoesNotExist:
        return HttpResponseNotFound("Pendaftaran tidak ada")

def get_berkases(request):
    id = request.GET.get("id")
    jenis = request.GET.get("jenis")
    try:
        pendaftaran = Pendaftaran.objects.get(pk=id)
        if pendaftaran.user != request.user and not request.user.asisten:
            return HttpResponseForbidden("Bukan pendaftar")
        berkases = pendaftaran.berkas_set.filter(jenis=jenis).order_by("uploaded_at")
        return JsonResponse({"status": 200, "berkases": [flat_berkas(b) for b in berkases]})
    except Berkas.DoesNotExist:
        return HttpResponseNotFound("Berkas tidak ada")

def get_berkas(request):
    id = request.GET.get("id")
    try:
        berkas = Berkas.objects.get(pk=id)
        if berkas.pendaftaran.user != request.user and not request.user.asisten:
            return HttpResponseForbidden("Bukan pendaftar")
        return JsonResponse({"status": 200, "berkas": flat_berkas(berkas)})
    except Berkas.DoesNotExist:
        return HttpResponseNotFound("Berkas tidak ada") 

def add_berkas(request):
    if request.method == "POST":
        id = request.POST.get("id")
        pendaftaran = Pendaftaran.objects.get(pk=id)
        if pendaftaran.user != request.user and not request.user.asisten:
            return HttpResponseForbidden("Bukan pendaftar")
        file = request.FILES["file"]
        pendaftaran.berkas_set.create(file=file, jenis=request.POST.get("jenis"))
        return JsonResponse({"status": 200})
    return JsonResponse({"status": -1})

def komentar_berkas(request):
    if request.method == "POST":
        id = request.POST.get("id")
        pendaftaran = Pendaftaran.objects.get(pk=id)
        if pendaftaran.user != request.user and not request.user.asisten:
            return HttpResponseForbidden("Bukan pendaftar")
        berkas_id = request.POST.get("berkas_id")
        berkas = pendaftaran.berkas_set.get(pk=berkas_id)
        berkas.komentar_set.create(content=request.POST.get("komentar"), user=request.user)
        berkas.save()
        return JsonResponse({"status": 200})
    return JsonResponse({"status": -1})
