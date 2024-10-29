from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("persyaratan/", views.persyaratan, name="persyaratan"),
    path("pendaftaran/", views.pendaftaran, name="pendaftaran"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("asisten/", views.asisten, name="asisten"),
    path("informasi/", views.informasi, name="informasi"),
    path("files/<int:id>", views.getFile, name="get_file"),
    path("filePersyaratan/", views.getFilePersyaratan, name="get_file_persyaratan"),
    path("pdf/", views.html_to_pdf_view, name="pdf"),
]
