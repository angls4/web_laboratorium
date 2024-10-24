from enum import verify
from math import e
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
import os
from dotenv import load_dotenv

from web_laboratorium.apps.app_auth.models import UMSUser
from .forms import UMSUserChangePasswordForm, UMSUserCreationForm,UMSUserAuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from web_laboratorium.apps.django_email_verification import (
    verify_email as verify_token,
    verify_password,
    verify_email_view,
    verify_password_view,
    send_email,
    send_password,
    default_token_generator
)

load_dotenv()
User = UMSUser
class Logout(auth_views.LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def register(request):
    alert = None
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UMSUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("verify_email", user_id=user.id)
            # auth_login(request, user)
            # return redirect("home")
    else:
        form = UMSUserCreationForm()
    return render(request, "register.html", {"form": form, "alert": alert})


def login(request):
    verify_link = None
    reset_link = None
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UMSUserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_verified:
                verify_link = f"/verify-email/{user.id}"
            else:
                auth_login(request, user)
                return redirect("home")
        else:
            reset_link = f"/reset-password/{form.cleaned_data.get('username')}"
    else:
        form = UMSUserAuthenticationForm()
    return render(request, "login.html", {"form": form, "verify_link": verify_link, "reset_link": reset_link})

def verify_email(request, user_id):

    try:
        user = User.objects.get(pk=user_id)
    except:
        return render(request, "email_sent.html", {"message": "User tidak ditemukan."})
    if user.is_verified:
        return render(request, "email_sent.html", {"message": "Email sudah diverifikasi."})
    try:
        send_email(user, thread=False, expiry=None, context=None)
        return render(request, "email_sent.html", {"message": "Email verifikasi telah dikirim."})
    except:
        return render(request, "email_not_sent.html", {"message": "Email verifikasi gagal dikirim.", "verify_link": f"/verify-email/{user_id}"})

@verify_email_view
def confirm_email(request, token):
    success, user = verify_token(token)
    return render(request, "email_success_template.html", {"success": success, "user": user, "message": "Email berhasil diverifikasi."})

def reset_password(request, email):
    try:
        user = User.objects.get(email=email)
    except:
        return render(request, "email_sent.html", {"message": "User tidak ditemukan."})
    try:
        send_password(user, thread=False, expiry=None, context=None)
        return render(request, "email_sent.html", {"message": "Email reset password telah dikirim."})
    except:
        return render(request, "email_not_sent.html", {"message": "Email reset password gagal dikirim.", "verify_link": f"/reset-password/{email}"})

@verify_password_view
def change_password(request, token):
    success_token, user = default_token_generator.check_token(token, kind="PASSWORD")
    if request.method == "POST":
        form = UMSUserChangePasswordForm(request.POST)
        is_verify = False
        if form.is_valid():
            password = form.cleaned_data.get("password")
            success, user = verify_password(token, password)
            if success:
                if user.is_verified == False:
                    user.is_verified = True
                    is_verify = True
                auth_login(request, user)
        else:
            return render(request, "password_change_template.html", {"form": form, "token": token, "user": user, "request": request})
        return render(request, "email_success_template.html", {"success": success, "user": user, "message": f"Password berhasil diubah{' dan user berhasil terverifikasi' if is_verify else ''}."})
    if not success_token:
        return render(request, "email_success_template.html", {"success": False, "user": user, "message": "."})
    return render(request, "password_change_template.html", {"form":UMSUserChangePasswordForm(), "token": token, "user": user, "request": request})

def login_admin(request):
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    try:
        admin_user = User.objects.get(email=admin_email)
    except User.DoesNotExist:
        admin_user = User.objects.create_user(email=admin_email, password=admin_password, first_name="Admin")
        admin_user.is_verified = True
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

    auth_logout(request)
    auth_login(request, admin_user)
    return redirect("home")
