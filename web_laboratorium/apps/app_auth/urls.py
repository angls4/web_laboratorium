from . import views
import os
from dotenv import load_dotenv
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views

load_dotenv()

urlpatterns = [
    # path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    # path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("logout/", views.Logout.as_view(next_page="home"), name="logout"),
    path("confirm-email/<str:token>/", views.confirm_email),
    path("verify-email/<str:user_id>", views.verify_email, name="verify_email"),
    path("change-password/<str:token>", views.change_password),
    path('reset-password/<str:email>', views.reset_password, name='reset_password'),
    path(f"{os.getenv('ADMIN_SECRET_URL','loginadmin')}/", views.login_admin, name="login_admin"),
]
