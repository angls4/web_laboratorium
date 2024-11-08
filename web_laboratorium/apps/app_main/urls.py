from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("persyaratan/<int:id>", views.persyaratan, name="persyaratan_detail"),
    path("persyaratan/", views.persyaratan, name="persyaratan"),
    path("pendaftaran/<int:id>", views.pendaftaran, name="edit_pendaftaran"),
    path("pendaftaran/", views.pendaftaran, name="pendaftaran"),
    path("pendaftaran/delete/<int:id>", views.delete_pendaftaran, name="delete_pendaftaran"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/pdf", views.dashboard_pdf, name="dashboard_pdf"),
    path("asisten/", views.asisten, name="asisten"),
    path("informasi/", views.informasi, name="informasi"),
    # path("files/<int:id>", views.getFile, name="get_file"),
    # path("file-persyaratan/", views.getFilePersyaratan, name="get_file_persyaratan"),
    path("send-loa/<int:pendaftaran_id>", views.send_loa, name="send_loa"),
]
