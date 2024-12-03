import datetime
import json
from django.http import HttpResponseForbidden, HttpResponseNotFound, JsonResponse

from web_laboratorium.apps.app_main.models import Asisten, Berkas, Pendaftaran, Praktikum
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
            filter_kwargs["persyaratan__praktikum"] = request.user.asisten.praktikum
        pendaftarans = Pendaftaran.objects.filter(deleted_at__isnull=True, **filter_kwargs).order_by(sort_by)
    else:
        pendaftarans = Pendaftaran.objects.filter(deleted_at__isnull=True, user=request.user)

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
    file_name = f'{request.user.first_name}_dashboard_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}.pdf'
    html_string = render_to_string("dashboard_pdf.html", pdf_context)
    return JsonResponse({"html_string": html_string, "status": 200, "file_name": file_name})

@login_required
@user_passes_test(lambda u: u.asisten)
def asisten_pdf(request):
    periode_filter = request.GET.get("periode") or ""
    praktikum_filter = request.GET.get("praktikum") or ""
    sort_by = request.GET.get("sort_by", "created_at")
    if not sort_by:
        sort_by = "created_at"
    order = request.GET.get("order", "asc")
    if not order:
        order = "asc"

    rows = Asisten.objects.all()
    for row in rows:
        row.nama = row.user.first_name
        row.nama_praktikum = row.praktikum.praktikum_name
    reversed_columns = ["nama", "nama_praktikum"]
    rows = sorted(
        rows,
        key=lambda x: x.__dict__[sort_by],
        reverse=True if order == ("desc" if sort_by not in reversed_columns else "asc") else False,
    )
    if periode_filter:
        rows = list(filter(lambda x: x.periode == periode_filter, rows))
        print(rows)
    if praktikum_filter:
        rows = list(filter(lambda x: x.nama_praktikum == praktikum_filter, rows))

    praktikum_options = Praktikum.objects.all()
    periode_options = range(2018, 2026)

    pdf_context = {
        "user": request.user,
        # "debug": True,
        "rows": rows,
        "praktikum_options": praktikum_options,
        "periode_options": periode_options,
        "periode_filter": periode_filter,
        "praktikum_filter": praktikum_filter,
        "date": datetime.datetime.now().strftime("%d %B %Y %H:%M"),
    }
    file_name = f'{request.user.first_name}_asisten_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}.pdf'
    html_string = render_to_string("asisten_pdf.html", pdf_context)
    return JsonResponse({"html_string": html_string, "status": 200, "file_name": file_name})
    

@login_required
@user_passes_test(lambda u: u.koordinator)
def next_status(request):
    id = request.POST.get("id")
    data = None
    try:
        data = json.loads(request.POST.get("data"))
    except:
        pass
    if id:
        nilai = None
        pendaftaran = Pendaftaran.objects.get(deleted_at__isnull=True, id=id)
        if data:
            nilai = pendaftaran.set_nilai_status(data)
        if pendaftaran.berkas_revision["unrevised"] > 0:
            return JsonResponse({"status": 400, "message": "Masih ada berkas yang belum direvisi"})
        new_status = pendaftaran.next_status()
        status = 200 if new_status else 400
        return JsonResponse({"status": status, "next_status": new_status, "nilai": nilai})
    return JsonResponse({"status": -1}, status=400)

@login_required
@user_passes_test(lambda u: u.koordinator)
def set_nilai(request,id):
    # id = request.POST.get("id")
    # status = request.POST.get("status")
    try:
        data = json.loads(request.body)
        if id and data:
            pendaftaran = Pendaftaran.objects.get(deleted_at__isnull=True, id=id)
            nilai = pendaftaran.set_nilai_status(data)
            return JsonResponse({"status": 200, "nilai": nilai})
    except:
        pass
    return JsonResponse({"status": -1}, status=400)

# def set_catatan(request):
#     id = request.POST.get("id")
#     catatan = request.POST.get("catatan")
#     status = request.POST.get("status")
#     if id and catatan and status:
#         pendaftaran = Pendaftaran.objects.get(deleted_at__isnull=True, id=id)
#         new_catatan = pendaftaran.set_catatan_status(catatan, status)
#         return JsonResponse({"status": 200, "catatan": new_catatan})
#     return JsonResponse({"status": -1}, status=400)

@login_required
def delete_pendaftaran(request):
    id = request.POST.get("id")
    try:
        pendaftaran = Pendaftaran.objects.get(deleted_at__isnull=True, pk=id)
        if pendaftaran.user != request.user and not request.user.koordinator:
            return HttpResponseForbidden("Bukan pendaftar")
        # pendaftaran.delete()
        pendaftaran.deleted_at = datetime.datetime.now()
        pendaftaran.save()
        return JsonResponse({"status": 200})
    except Pendaftaran.DoesNotExist:
        return HttpResponseNotFound("Pendaftaran tidak ada")


@login_required
def get_berkasesList(request):
    id = request.GET.get("id")
    try:
        pendaftaran = Pendaftaran.objects.get(deleted_at__isnull=True, pk=id)
        if pendaftaran.user != request.user and not request.user.asisten:
            return HttpResponseForbidden("Bukan pendaftar")
        # berkases = pendaftaran.berkas_set.all()
        berkasesList = []
        for jenis_value,jenis_label in Berkas.jenis_choices:
            item = {
                "label": jenis_label,
                "value": jenis_value,
                "berkases": [],
                "revision": pendaftaran.jenis_revision(jenis_value),
            }
            try:
                berkases = pendaftaran.berkas_set.filter(jenis=jenis_value).order_by("uploaded_at").reverse()
                item["berkases"] = [
                    berkas.getDict()
                    for berkas in berkases
                ]
            except Berkas.DoesNotExist:
                pass
            berkasesList.append(item)
        return JsonResponse({"status": 200, "berkasesList": berkasesList})
    except Pendaftaran.DoesNotExist:
        return HttpResponseNotFound("Pendaftaran tidak ada")

@login_required
def get_berkases(request):
    id = request.GET.get("id")
    jenis = request.GET.get("jenis")
    if id and jenis:
        try:
            pendaftaran = Pendaftaran.objects.get(deleted_at__isnull=True, pk=id)
            if pendaftaran.user != request.user and not request.user.asisten:
                return HttpResponseForbidden("Bukan pendaftar")
            berkases = pendaftaran.berkas_set.filter(jenis=jenis).order_by("uploaded_at").reverse()
            print(berkases)
            return JsonResponse(
                {
                    "status": 200,
                    "berkas_revision": pendaftaran.berkas_revision,
                    "revision": pendaftaran.jenis_revision(jenis),
                    "berkases": [berkas.getDict() for berkas in berkases],
                }
            )
        except Berkas.DoesNotExist:
            return HttpResponseNotFound("Berkas tidak ada")
    return JsonResponse({"status": -1}, status=400)

@login_required
def get_berkas(request):
    id = request.GET.get("id")
    try:
        berkas = Berkas.objects.get(pk=id)
        pendaftaran = berkas.pendaftaran
        if pendaftaran.user != request.user and not request.user.asisten:
            return HttpResponseForbidden("Bukan pendaftar")
        return JsonResponse(
            {
                "status": 200,
                "berkas_revision": pendaftaran.berkas_revision,
                "revision": pendaftaran.jenis_revision(berkas.jenis),
                "berkas": berkas.getDict(),
            }
        )
    except Berkas.DoesNotExist:
        return HttpResponseNotFound("Berkas tidak ada")

@login_required
def get_pendafataran(request):
    id = request.GET.get("id")
    try:
        pendaftaran = Pendaftaran.objects.get(deleted_at__isnull=True, pk=id)
        if pendaftaran.user != request.user and not request.user.asisten:
            return HttpResponseForbidden("Bukan pendaftar")
        return JsonResponse(
            {
                "status": 200,
                "pendaftaran": pendaftaran.getDict(),
            }
        )
    except Pendaftaran.DoesNotExist:
        return HttpResponseNotFound("Pendaftaran tidak ada")

@login_required
def add_berkas(request):
    id = request.POST.get("id")
    jenis = request.POST.get("jenis")
    if id and jenis:
        pendaftaran = Pendaftaran.objects.get(deleted_at__isnull=True, pk=id)
        if pendaftaran.user != request.user and not request.user.asisten:
            return HttpResponseForbidden("Bukan pendaftar")
        file = request.FILES["file"]
        pendaftaran.berkas_set.create(file=file, jenis=jenis)
        pendaftaran.edited_at = datetime.datetime.now()
        pendaftaran.save()
        return JsonResponse({"status": 200})
    return JsonResponse({"status": -1}, status=400)

@login_required
def komentar_berkas(request):
    id = request.POST.get("id")
    komentar = request.POST.get("komentar")
    if id and komentar:
        berkas = Berkas.objects.get(pk=id)
        pendaftaran = berkas.pendaftaran
        if pendaftaran.user != request.user and not request.user.asisten:
            return HttpResponseForbidden("Bukan pendaftar")
        berkas.komentar_set.create(content=komentar, user=request.user)
        berkas.save()
        return JsonResponse({"status": 200})
    return JsonResponse({"status": -1}, status=400)
