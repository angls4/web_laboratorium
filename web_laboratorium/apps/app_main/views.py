import json
from multiprocessing import context
from threading import Thread
from webbrowser import get
from django.shortcuts import redirect, render
from django.http import HttpResponseNotFound
from django.conf import settings
from django.template import Context, Template

from web_laboratorium.apps.app_main.loa import loa_attatchment
from .forms import FormPersyaratan, UploadPendaftaran, UpdatePendaftaran
from .models import Pendaftaran, Persyaratan, Praktikum, NILAI_CHOICES
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from django.forms import formset_factory
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string

from django.contrib.auth import get_user_model
from .models import Asisten
from django.http import JsonResponse

User = get_user_model()

def send_email_thread(targets, subject, text_path, html_path = None, context = None, attatchments = None):
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
    if attatchments:
        for attatchment in attatchments:
            mail.attach(*attatchment)
    mail.send()


def send_email(targets, subject, html_path = None, context=None, thread=True, text_path=None, attatchments=None):
    if thread:
        t = Thread(target=send_email_thread, args=(targets, subject, text_path, html_path, context, attatchments))
        t.start()
    else:
        send_email_thread(targets, subject, text_path, html_path, context, attatchments)

def send_status_email(user, pendaftaran, newStatus, thread=True):    
    subject = "Status Pendaftaran Praktikum"
    context = {
        "nama": user.first_name,
        "praktikum": pendaftaran.praktikum.praktikum_name,
        "status": newStatus,
    }
    send_email([user.email], subject, "email/status_email.html", context, thread)


# Rest of the code

def index(req):
    return render(req, "home.html")

def informasi(req):
    return render(req, "informasi.html", {"html_string" : render_to_string('email/pengumuman_email.html')})

# def persyaratan(request):
#     try:
#         persyaratan = Persyaratan.objects.filter(active=True, pengumuman__lte=datetime.datetime.now()).latest('uploaded_at')
#     except Persyaratan.DoesNotExist:
#         persyaratan = None
#     return render(request, "persyaratan.html", {"file": persyaratan})
def persyaratan(request, id=None):
    if request.user.is_anonymous:
        request.user.asisten = getattr(request.user, "asisten", False)
    persyaratan = None
    persyaratans = []
    if request.user.asisten:
        try:
            persyaratans = Persyaratan.objects.filter(active=True)
        except:
            pass
    if not id:
        try:
            persyaratan = Persyaratan.objects.filter(active=True, pengumuman__gte=datetime.datetime.now()).latest('uploaded_at')
            # if request.user.asisten:
            #     persyaratan = None
            #     context = {
            #         "form": FormPersyaratan(),
            #         "persyaratan": None,
            #         "persyaratans": persyaratans,
            #     }
            #     return render(request, "persyaratan.html", context)
            if not request.user.asisten:
                return redirect("persyaratan_detail", id=persyaratan.id)
                # if persyaratan:
                # else:
                #     return render(request, "persyaratan.html")
        except Persyaratan.DoesNotExist:
            pass
    try:
        persyaratan = Persyaratan.objects.get(pk=id)
        context = {
            "form" : FormPersyaratan(instance=persyaratan),
            "persyaratan": persyaratan,
        }
        # return render(request, "persyaratan_detail.html", context=context)
    except Persyaratan.DoesNotExist:
        if persyaratan:
            persyaratan.pk = None
        context = {
            "form": FormPersyaratan(),
            "persyaratan": persyaratan,
        }
        persyaratan = None

    if request.method == "POST":
        # print(request.user.id)
        if(request.POST.get("delete") is not None):
            try:
                persyaratan.active = False
                persyaratan.save()
            except:
                context["delete_failed"] = True
            # try:
            #     file_path = settings.PERSYARATAN_PATH
            #     os.remove(file_path)
            #     context["delete_success"] = True
            # except FileNotFoundError:
            #     context["delete_failed"] = True
            return redirect("persyaratan")
        form = FormPersyaratan(request.POST, request.FILES, instance=persyaratan)
        if form.is_valid():
            form = form.save(commit=False)
            context = {
                "form": FormPersyaratan(instance=form),
                "persyaratan": form,
            }
            context["upload_success"] = True
            context["persyaratans"] = persyaratans
            return render(request, "persyaratan.html", context)
        else:
            context["invalid"] = True
    print(context)
    context["persyaratans"] = persyaratans
    return render(request, "persyaratan.html", context)


@login_required
def pendaftaran(request,id=None):
    context = {}
    if id:
        try:
            pendaftaran = Pendaftaran.objects.get(pk=id)
            if pendaftaran.user != request.user and not request.user.koordinator:
                return HttpResponseForbidden("Bukan pendaftar")
            context = {
                "form": UploadPendaftaran(instance=pendaftaran, request=request),
                "file": pendaftaran,
            }
        except Pendaftaran.DoesNotExist:
            return HttpResponseNotFound("Pendaftaran tidak ada")
    else:
        context["form"] = UploadPendaftaran(request=request)
    if request.method == "POST":
        form = UploadPendaftaran(request.POST, request.FILES, request=request, instance=pendaftaran if id else None)
        context["form"] = form
        if form.is_valid():
            form = form.save(edited=id)
            # form = form.save(commit=False)
            # form.user = request.user
            # current_year = datetime.datetime.now().strftime("%Y")
            # form.berkas.name = f"{request.user.nim}_{form.praktikum}_{current_year}.{form.file.name.split('.')[-1]}"
            # form.save()
            context["upload_success"] = True
            context["form"] = UploadPendaftaran(request=request, instance=form)
            # return render(request, "pendaftaran.html", context)
            return redirect("dashboard")
        else:
            context["invalid"] = True
            return render(request, "pendaftaran.html", context)
    else:
        return render(request, "pendaftaran.html", context)



# @login_required
# def dashboard(request):
#     print(request.user.asisten)
#     print(request.user.koordinator)
#     tahun_filter = request.GET.get('tahun') or ''
#     nilai_filter = request.GET.get('nilai') or ''
#     status_filter = request.GET.get('status') or ''
#     sort_by = request.GET.get('sort_by', 'uploaded_at') or 'uploaded_at'
#     order = request.GET.get('order', 'asc') or 'asc'

#     updatePendaftaranFactory = formset_factory(UpdatePendaftaran, extra=0)
#     if request.user.asisten:
#         if request.method == "POST":
#             formSet = updatePendaftaranFactory(request.POST)
#             if formSet.is_valid():
#                 for form in formSet.forms:
#                     if form.cleaned_data:
#                         pendaftaran = Pendaftaran.objects.get(id=form.cleaned_data["id"])
#                         if form.cleaned_data["selection_status"]:
#                             # print(pendaftaran.status, form.cleaned_data["selection_status"])
#                             if pendaftaran.status != int(form.cleaned_data["selection_status"]):
#                                 status_label = dict(form.fields["selection_status"].choices)[int(form.cleaned_data["selection_status"])]
#                                 send_status_email(pendaftaran.user, pendaftaran, status_label)
#                                 # try:
#                                 # except:
#                                 #     print("Email failed to send", f'{pendaftaran.user.email} {form.cleaned_data["selection_status"]}')
#                             pendaftaran.selection_status = form.cleaned_data["selection_status"]
#                             pendaftaran.save()
#                         # print(pendaftaran.status)
#                         pendaftaran = Pendaftaran.objects.get(id=form.cleaned_data["id"])
#                         if pendaftaran.status == 6:
#                             # pendaftaran.user.is_staff = True
#                             # pendaftaran.user.save()
#                             if not Asisten.objects.filter(user=pendaftaran.user, praktikum=pendaftaran.praktikum).exists():
#                                 asisten = Asisten.objects.create(user=pendaftaran.user, praktikum=pendaftaran.praktikum, periode=pendaftaran.uploaded_at.year)
#                                 praktikum_periode = f"{pendaftaran.praktikum.praktikum_name} {asisten.periode}"
#                                 send_email(
#                                     [pendaftaran.user.email],
#                                     f"PENGUMUMAN TAHAP AKHIR OPEN RECRUITMENT ASISTEN {praktikum_periode}",
#                                     "email/pengumuman_email.html",
#                                     {
#                                         "praktikum": pendaftaran.praktikum,
#                                         "praktikum_periode": praktikum_periode,
#                                     },
#                                     attatchments=[loa_attatchment(pendaftaran)]
#                                 )
#         files = Pendaftaran.objects.all()
#         if tahun_filter:
#             files = list(filter(lambda x: x.uploaded_at.year == int(tahun_filter), files))
#         if nilai_filter:
#             files = list(filter(lambda x: x.nilai == nilai_filter, files))
#         if status_filter:
#             files = list(filter(lambda x: x.status == int(status_filter), files))
#         if not request.user.is_superuser:
#             files = list(filter(lambda x: (x.praktikum) == request.user.asisten.praktikum, files))
#         initial_data = []
#         for file in files:
#             # file.nama_praktikum = file.praktikum.praktikum_name
#             file.nim = file.user.nim
#             file.nama = file.user.first_name
#             initial_data.append(
#                 {
#                     "id": file.id,
#                     "selection_status": file.status,
#                 }
#             )
#         formSet = updatePendaftaranFactory(initial=initial_data)
#         for form in formSet:
#             status_choices = dict(form.fields["selection_status"].choices)
#             form.fields["selection_status"].choices = [
#                 (key, value) for key, value in status_choices.items()
#                 if key == form.initial["selection_status"] or key == form.initial["selection_status"] + 1 or key == -1
#             ]
#             if form.initial["selection_status"] == 6 or form.initial["selection_status"] == -1:
#                 form.fields["selection_status"].widget.attrs["disabled"] = "disabled"
#         # formSet = updatePendaftaranFactory(queryset = files)``
#         rows = [{"file": file,"form": form} for file, form in zip(files, formSet)]
#         context = {
#             "rows": rows,
#             "formSet": formSet,
#         }
#     else:
#         files = Pendaftaran.objects.filter(user=request.user)
#         rows = [{"file": file,"form": ''} for file in files]
#         context = {
#             "rows": rows,
#         }
#     reversed_columns = ['nama', 'nim', 'nilai']
#     rows = sorted(rows, key=lambda x: x["file"].__dict__[sort_by], reverse=True if order == ('desc' if sort_by not in reversed_columns else 'asc') else False)

#     context["rows"] = rows

#     tahun_options = range(2018, 2026)
#     nilai_options = [{"value": str(choice[0]), "label": choice[1]} for choice in NILAI_CHOICES]
#     status_options = [{"value": str(choice[0]), "label": choice[1]} for choice in Pendaftaran.STATUS_CHOICES]

#     jabatan = 'Admin' if request.user.is_superuser else 'Koordinator' if request.user.koordinator else 'Asisten' if request.user.asisten else 'Peserta'
#     context.update({
#         "tahun_options": tahun_options,
#         "nilai_options": nilai_options,
#         "status_options": status_options,
#         "jabatan": jabatan
#     })
#     context["html_string"] = render_to_string("dashboard_pdf.html", {
#         "user": request.user,
#         "rows": rows,
#         "date": datetime.datetime.now().strftime("%d %B %Y %H:%M"),
#         "tahun_filter": tahun_filter,
#         "nilai_filter": nilai_filter,
#         "status_filter": dict(Pendaftaran.STATUS_CHOICES)[int(status_filter)] if status_filter else '',
#         "jabatan": jabatan
#     })

#     context["items_json"] = [
#         {"id": i, "name": f"Dummy {i}"} for i in range(1, 21)
#     ]
#     context["debug"] = True
#     context["rows_json"] = [
#         {
#             "id": row["file"].id,
#             "nim": row["file"].nim,
#             "nama": row["file"].nama,
#             "sosial_media": row["file"].sosial_media,
#             "file": row["file"].file.url if row["file"].file else None,
#             "tanggal": row["file"].tanggal.strftime("%Y-%m-%d %H:%M:%S") if row["file"].tanggal else None,
#             "tanggal_edit": row["file"].tanggal_edit.strftime("%Y-%m-%d %H:%M:%S") if row["file"].tanggal_edit else None,
#             "ipk": row["file"].ipk,
#             "nilai_praktikum": row["file"].nilai_praktikum,
#             "status": row["file"].status,
#             "uploaded_at": row["file"].uploaded_at.strftime("%Y-%m-%d %H:%M:%S"),
#         }
#         for row in rows
#     ]
#     return render(request, 'dashboard.html', context)

@login_required
def dashboard(request):
    filter_kwargs = {}
    sort_by = 'uploaded_at'
    if request.user.asisten:
        if not request.user.is_superuser:
            filter_kwargs["praktikum"] = request.user.asisten.praktikum
        pendaftarans = Pendaftaran.objects.filter(**filter_kwargs).order_by(sort_by)
    else:
        pendaftarans = Pendaftaran.objects.filter(user=request.user)

    rows = []
    for pendaftaran in pendaftarans:
        rows.append({
            "id": pendaftaran.id,
            "nim": pendaftaran.user.nim,
            "nama": pendaftaran.user.first_name,
            "linkedin": pendaftaran.linkedin,
            "instagram": pendaftaran.instagram,
            "file": pendaftaran.file.url if pendaftaran.file else None,
            "uploaded_at_int": int(pendaftaran.uploaded_at.timestamp()),
            "tahun": pendaftaran.uploaded_at.year,
            "uploaded_at": pendaftaran.uploaded_at.strftime("%Y-%m-%d"),
            "edited_at": pendaftaran.edited_at.strftime("%Y-%m-%d") if pendaftaran.edited_at else '-',
            "ipk": str(pendaftaran.ipk),
            "nilai_id": pendaftaran.nilai,
            "nilai": pendaftaran.get_nilai_display(),
            "status_id": pendaftaran.status,
            "status": pendaftaran.get_selection_status_display(),
            "berkas_revision": pendaftaran.berkas_revision,
        })
 
    tahun_options = list(range(2018, 2026))
    nilai_options = [{"value": str(choice[0]), "label": choice[1]} for choice in NILAI_CHOICES]
    status_options = [{"value": str(choice[0]), "label": choice[1]} for choice in Pendaftaran.STATUS_CHOICES]
    context = {
        "user": request.user.get_dict(),
        # "debug": True,
        "rows": rows,
        "tahun_options": tahun_options,
        "nilai_options": nilai_options,
        "status_options": status_options,
    }

    return render(request, 'dashboard.html', {"debug":True, "context": json.dumps(context)})


    
    # return render(request, 'dashboard.html', {"debug":True, "context": json.dumps(context)})


# @login_required
# def getFile(request, id):
#     try:
#         file = Pendaftaran.objects.get(pk=id)
#         if file.user == request.user or request.user.asisten:
#             response = FileResponse(open(file.file.path, "rb"))
#             return response
#         else:
#             return HttpResponseForbidden("You are not authorized to access this file.")
#     except Pendaftaran.DoesNotExist:
#         return HttpResponseNotFound("File not found.")

# def getFilePersyaratan(request):
#     try:
#         current_active = Persyaratan.objects.filter(active=True).latest('uploaded_at')
#         if not current_active:
#             return HttpResponseNotFound("File not found.")
#         response = FileResponse(open(current_active.file.path, "rb"))
#         return response
#     except FileNotFoundError:
#         return HttpResponseNotFound("File not found.")

@user_passes_test(lambda user: user.is_superuser)
def asisten(request):
    periode_filter = request.GET.get('periode') or ''
    praktikum_filter = request.GET.get('praktikum') or ''
    sort_by = request.GET.get('sort_by', 'created_at')
    if not sort_by:
               sort_by = "created_at"
    order = request.GET.get('order', 'asc')
    if not order:
        order = 'asc'

    rows = Asisten.objects.all()
    for row in rows:
        row.nama = row.user.first_name
        row.nama_praktikum = row.praktikum.praktikum_name
    reversed_columns = ["nama", "nama_praktikum"]
    rows = sorted(rows, key=lambda x: x.__dict__[sort_by], reverse=True if order == ('desc' if sort_by not in reversed_columns else 'asc') else False)
    if periode_filter:
        rows = list(filter(lambda x: x.periode == periode_filter, rows))
        print(rows)
    if praktikum_filter:
        rows = list(filter(lambda x: x.nama_praktikum == praktikum_filter, rows))

    praktikum_options = Praktikum.objects.all()
    periode_options = range(2018, 2026)

    context = {
        "rows": rows,
        "praktikum_options": praktikum_options,
        "periode_options": periode_options,
    }
    context["html_string"] = render_to_string("asisten_pdf.html", {
        "rows": rows,
        "date": datetime.datetime.now().strftime("%d %B %Y %H:%M"),
        "periode_filter": periode_filter,
        "praktikum_filter": praktikum_filter,
    })
    return render(request, 'asisten.html', context)

@user_passes_test(lambda user: user.koordinator)
def send_loa(request, pendaftaran_id):
    if not request.user.is_anonymous and not request.user.koordinator:
        return HttpResponseForbidden("You are not authorized to access this page.")
    try:
        pendaftaran = Pendaftaran.objects.get(pk=pendaftaran_id)
        if pendaftaran.status == 6:
            try:
                send_email(
                    [pendaftaran.user.email],
                    f"Pengiriman Ulang Letter of Acceptance {pendaftaran.persyaratan}",
                    "email/loa_email.html",
                    {
                        "pendaftaran": pendaftaran,
                    },
                    attatchments=[loa_attatchment(pendaftaran)],
                )
            except:
                return render(request, "email_not_sent.html", {"message": "Email LOA gagal dikirim.", "verify_link": f"/send-loa/{pendaftaran_id}"})
            return render(request, "email_sent.html", {"message": "Email LOA telah dikirim.", "redirect_to": "close"})
        else:
            return HttpResponseForbidden("Pendaftaran status is not valid for sending LOA.")
    except Pendaftaran.DoesNotExist:
        return HttpResponseNotFound("Pendaftaran not found.")
