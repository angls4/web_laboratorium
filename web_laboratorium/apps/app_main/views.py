import os
from urllib import response
from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.conf import settings
from .forms import UploadPersyaratan, UploadPendaftaran, UpdatePendaftaran
from .models import Pendaftaran, Persyaratan, Praktikum
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from django.forms import formset_factory
from django.http import HttpResponseForbidden, FileResponse
from django.contrib.auth import get_user_model
from .models import Asisten

User = get_user_model()

# Rest of the code

def index(req):
    return render(req, "home.html")

def informasi(req):
    return render(req, "informasi.html")

def persyaratan(request):
    try:
        current_active = Persyaratan.objects.filter(active=1).latest('uploaded_at')
    except:
        current_active = None
    context = {
        "form": UploadPersyaratan(),
        # "PERSYARATAN_URL": request.build_absolute_uri("/")[:-1] + settings.MEDIA_URL + settings.PERSYARATAN_URL,
        # "PERSYARATAN_URL": current_active.file.url if current_active else None,
        "PERSYARATAN_URL": "/filePersyaratan",
    }
    if request.method == "POST":
        # print(request.user.id)
        if(request.POST.get("delete") is not None):
            try:
                current_active.active = False
                current_active.save()
            except:
                context["delete_failed"] = True
            # try:
            #     file_path = settings.PERSYARATAN_PATH
            #     os.remove(file_path)
            #     context["delete_success"] = True
            # except FileNotFoundError:
            #     context["delete_failed"] = True
            return render(request, "persyaratan.html", context)
        form = UploadPersyaratan(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            if current_active:
                current_active.active = False
                current_active.save()
            # print(form.files[0].name)
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            form.file.name = f"{current_datetime}.{form.file.name}"
            form.save()
            context["upload_success"] = True
            return render(request, "persyaratan.html", context)
        else:
            context["invalid"] = True
            return render(request, "persyaratan.html", context)
    else:
        return render(request, "persyaratan.html", context)


@login_required
def pendaftaran(request):
    context = {"form": UploadPendaftaran(request=request)}
    if request.method == "POST":
        form = UploadPendaftaran(request.POST, request.FILES, request=request)
        context["form"] = form
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            form.file.name = f"{request.user.email.split('@')[0]}_{form.praktikum}_{current_datetime}.{form.file.name.split('.')[-1]}"
            form.save()
            context["upload_success"] = True
            return render(request, "pendaftaran.html", context)
        else:
            context["invalid"] = True
            return render(request, "pendaftaran.html", context)
    else:
        return render(request, "pendaftaran.html", context)

@login_required
def dashboard(request):
    sort_by = request.GET.get('sort_by', 'uploaded_at')
    order = request.GET.get('order', 'asc')

    getFile_url = request.build_absolute_uri('/') + "files/"
    updatePendaftaranFactory = formset_factory(UpdatePendaftaran, extra=0)
    if request.user.is_staff:
        if request.method == "POST":
            formSet = updatePendaftaranFactory(request.POST)
            if formSet.is_valid():
                for form in formSet.forms:
                    # print(form.cleaned_data['status'])
                    if form.cleaned_data:
                        instance = Pendaftaran.objects.get(id=form.cleaned_data["id"])
                        if form.cleaned_data['status']:
                            instance.status = form.cleaned_data['status']
                            instance.save()
                        # print(instance.status)
                        if instance.status == "diterima":
                            instance.user.is_staff = True
                            instance.user.save()
                            if not Asisten.objects.filter(user=instance.user, praktikum=instance.praktikum).exists():
                                Asisten.objects.create(user=instance.user, praktikum=instance.praktikum)
        files = Pendaftaran.objects.all()
        initial_data = []
        for file in files:
            file.nim = file.user.email.split("@")[0]
            file.nama_praktikum = file.praktikum.practicum_name
            file.nama = file.user.first_name
            initial_data.append({
                "id": file.id,
                "status": file.status,
            })
        formSet = updatePendaftaranFactory(initial=initial_data)
        for form in formSet:
            if form.initial["status"] == "diterima":
                form.fields["status"].widget.attrs["disabled"] = "disabled"
        # formSet = updatePendaftaranFactory(queryset = files)``
        rows = [{"file": file,"form": form} for file, form in zip(files, formSet)]
        context = {
            "getFile_url": getFile_url,
            "rows": rows,
            "formSet": formSet,
        }
    else:
        files = Pendaftaran.objects.filter(user=request.user)
        rows = [{"file": file,"form": ''} for file in files]
        context = {
            "getFile_url": getFile_url,
            "rows": rows,
        }

    context["rows"] = sorted(context["rows"], key=lambda x: x["file"].__dict__[sort_by], reverse=True if order == 'desc' else False)
    return render(request, 'dashboard.html', context)


@login_required
def getFile(request, id):
    try:
        file = Pendaftaran.objects.get(pk=id)
        if file.user == request.user or request.user.is_staff:
            response = FileResponse(open(file.file.path, "rb"))
            return response
        else:
            return HttpResponseForbidden("You are not authorized to access this file.")
    except Pendaftaran.DoesNotExist:
        return HttpResponseNotFound("File not found.")

def getFilePersyaratan(request):
    try:
        current_active = Persyaratan.objects.filter(active=True).latest('uploaded_at')
        if not current_active:
            return HttpResponseNotFound("File not found.")
        response = FileResponse(open(current_active.file.path, "rb"))
        return response
    except FileNotFoundError:
        return HttpResponseNotFound("File not found.")

@user_passes_test(lambda user: user.is_superuser)
def asisten(request):
    periode_filter = request.GET.get('periode', None)
    praktikum_filter = request.GET.get('praktikum', None)
    sort_by = request.GET.get('sort_by', 'created_at')
    if not sort_by:
        sort_by = 'nama'
    order = request.GET.get('order', 'asc')
    if not order:
        order = 'asc'

    rows = Asisten.objects.all()
    for row in rows:
        row.nama = row.user.first_name
        row.nama_praktikum = row.praktikum.practicum_name
    rows = sorted(rows, key=lambda x: x.__dict__[sort_by], reverse=True if order == 'desc' else False)
    if periode_filter:
        rows = filter(lambda x: x.periode == periode_filter, rows)
    if praktikum_filter:
        rows = filter(lambda x: x.nama_praktikum == praktikum_filter, rows)

    praktikum_options = Praktikum.objects.all()
    periode_options = range(2018, 2026)

    context = {
        "rows": rows,
        "praktikum_options": praktikum_options,
        "periode_options": periode_options,
    }
    return render(request, 'asisten.html', context)
