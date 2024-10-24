from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from web_laboratorium.apps.app_main.models import Asisten, Pendaftaran, Praktikum
from .models import UMSUser

admin.site.register(UMSUser)
admin.site.register(Pendaftaran)
admin.site.register(Asisten)
admin.site.register(Praktikum)
