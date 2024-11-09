from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views
from . import api

urlpatterns = [
    path("", views.index, name="home"),
    path("persyaratan/<int:id>", views.persyaratan, name="persyaratan_detail"),
    path("persyaratan/", views.persyaratan, name="persyaratan"),
    path("pendaftaran/<int:id>", views.pendaftaran, name="edit_pendaftaran"),
    path("pendaftaran/", views.pendaftaran, name="pendaftaran"),
    # path("pendaftaran/delete/<int:id>", views.delete_pendaftaran, name="delete_pendaftaran"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api/pendaftaran/pdf", api.dashboard_pdf, name="api_pendaftaran_pdf"),
    path("api/pendaftaran/next-status", api.next_status, name="api_next_status"),
    path("api/pendaftaran/set-nilai", api.set_nilai, name="api_set_nilai"),
    path("api/pendaftaran/set-catatan", api.set_catatan, name="api_set_catatan"),
    path("api/pendaftaran/delete", api.delete_pendaftaran, name="api_delete_pendaftaran"),
    path("api/berkasesList", api.get_berkasesList, name="api_get_berkasesList"),
    path("api/berkases", api.get_berkases, name="api_get_berkases"),
    path("api/berkas", api.get_berkas, name="api_get_berkas"),
    path("api/berkas/add", api.add_berkas, name="api_add_berkas"),
    path("api/berkas/komen", api.komentar_berkas, name="api_komentar_berkas"),
    path("asisten/", views.asisten, name="asisten"),
    path("informasi/", views.informasi, name="informasi"),
    # path("files/<int:id>", views.getFile, name="get_file"),
    # path("file-persyaratan/", views.getFilePersyaratan, name="get_file_persyaratan"),
    path("send-loa/<int:pendaftaran_id>", views.send_loa, name="send_loa"),
]
