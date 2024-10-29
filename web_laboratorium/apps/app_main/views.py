from cgitb import text
from io import BytesIO
import os
from random import choice
from threading import Thread
from tkinter import E
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from django.template import Context, Template
import pdfkit
from .forms import UploadPersyaratan, UploadPendaftaran, UpdatePendaftaran
from .models import Pendaftaran, Persyaratan, Praktikum
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from django.forms import formset_factory
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseForbidden, FileResponse
from django.template.loader import render_to_string

from django.contrib.auth import get_user_model
from .models import Asisten

User = get_user_model()


def send_email_thread(targets, subject, text_path, html_path, context = None):
    sender = settings.EMAIL_FROM_ADDRESS
    if context is None:
        context = {}
    if settings.EMAIL_DESTINATION:
        targets = [settings.EMAIL_DESTINATION]

    subject = Template(subject).render(Context(context))
    try:
        html = render_to_string(html_path, context)
    except:
        html = None
    try:
        text = render_to_string(text_path, context)
    except:
        text = html

    mail = EmailMultiAlternatives(subject, text, sender, targets)
    if html:
        mail.attach_alternative(html, "text/html")
    mail.send()


def send_email(targets, subject, html_path, context=None, thread=True, text_path=None):
    if thread:
        t = Thread(target=send_email_thread, args=(targets, subject, text_path, html_path, context))
        t.start()
    else:
        send_email_thread(targets, subject, text_path, html_path, context)

def send_status_email(user, pendaftaran, newStatus, thread=True):    
    subject = "Status Pendaftaran Praktikum"
    context = {
        "nama": user.first_name,
        "praktikum": pendaftaran.praktikum.practicum_name,
        "status": newStatus,
    }
    send_email([user.email], subject, "email/status_email.html", context, thread)


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
    tahun_filter = request.GET.get('tahun', None)
    nilai_filter = request.GET.get('nilai', None)
    status_filter = request.GET.get('status', None)
    sort_by = request.GET.get('sort_by', 'uploaded_at') or 'uploaded_at'
    order = request.GET.get('order', 'asc') or 'asc'

    getFile_url = request.build_absolute_uri('/') + "files/"
    updatePendaftaranFactory = formset_factory(UpdatePendaftaran, extra=0)
    if request.user.is_staff:
        if request.method == "POST":
            formSet = updatePendaftaranFactory(request.POST)
            if formSet.is_valid():
                for form in formSet.forms:
                    # print(form.cleaned_data['status'])
                    if form.cleaned_data:
                        pendaftaran = Pendaftaran.objects.get(id=form.cleaned_data["id"])
                        if form.cleaned_data['status']:
                            if pendaftaran.status != int(form.cleaned_data["status"]):
                                status_label = dict(form.fields['status'].choices)[int(form.cleaned_data['status'])]
                                send_status_email(pendaftaran.user, pendaftaran, status_label)
                                # try:
                                # except:
                                #     print("Email failed to send", f'{pendaftaran.user.email} {form.cleaned_data["status"]}')
                            pendaftaran.status = form.cleaned_data['status']
                            pendaftaran.save()
                        # print(pendaftaran.status)
                        if pendaftaran.status == 11:
                            pendaftaran.user.is_staff = True
                            pendaftaran.user.save()
                            if not Asisten.objects.filter(user=pendaftaran.user, praktikum=pendaftaran.praktikum).exists():
                                Asisten.objects.create(user=pendaftaran.user, praktikum=pendaftaran.praktikum, periode=pendaftaran.uploaded_at.year)
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
            status_choices = dict(form.fields["status"].choices)
            form.fields["status"].choices = [
                (key, value) for key, value in status_choices.items()
                if key == form.initial["status"] or key == form.initial["status"] + 1 or key == -1
            ]
            if form.initial["status"] == 11:
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
    rows = sorted(rows, key=lambda x: x["file"].__dict__[sort_by], reverse=True if order == 'desc' else False)
    if tahun_filter:
        rows = filter(lambda x: x["file"].uploaded_at.year == int(tahun_filter), rows)
    if nilai_filter:
        rows = filter(lambda x: x["file"].nilai == nilai_filter, rows)
    if status_filter:
        rows = filter(lambda x: x["file"].status == int(status_filter), rows)
    context["rows"] = rows

    tahun_options = range(2018, 2026)
    nilai_options = [{"value": str(choice[0]), "label": choice[1]} for choice in Pendaftaran.NILAI_CHOICES]
    status_options = [{"value": str(choice[0]), "label": choice[1]} for choice in Pendaftaran.STATUS_CHOICES]

    context.update({
        "tahun_options": tahun_options,
        "nilai_options": nilai_options,
        "status_options": status_options,
    })

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
        sort_by = "created_at"
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


def html_to_pdf_view(request):
    # Define your HTML content
    # html_string = """
    #     <html>
    #     <head><title>Test PDF</title></head>
    #     <body>
    #         <h1>Hello, PDF!</h1>
    #         <p>This is a test PDF generated from HTML.</p>
    #     </body>
    #     </html>
    # """

    html_string = render_to_string("home.html", {"nama": "Test", "praktikum": "Test Praktikum", "status": "Test Status", "site_url": settings.SITE_URL})

    # Configure pdfkit options
    options = {
        "page-size": "Letter",
        "encoding": "UTF-8",
    }

    # Set wkhtmltopdf path if defined in settings
    config = (
        pdfkit.configuration(wkhtmltopdf=settings.PDFKIT_WKHTMLTOPDF)
        if hasattr(settings, "PDFKIT_WKHTMLTOPDF")
        else None
    )

    # Generate PDF as a blob in memory
    # pdf_blob = BytesIO()
    pdf_blob = pdfkit.from_string(html_string, options=options)

    # Seek to the beginning of the BytesIO buffer
    # pdf_blob.seek(0)

    # Create a response object and serve the PDF
    response = HttpResponse(pdf_blob, content_type="application/pdf")
    response["Content-Disposition"] = (
        'inline; filename="output.pdf"'  # Use 'attachment' instead of 'inline' to force download
    )

    return response
