import datetime
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class CustomUMSStudentEmailValidator(RegexValidator):
    regex = r"^[a-zA-Z]\d{9}@student\.ums\.ac\.id$"
    message = _("Enter a valid UMS student email address.")
    flags = 0

    def __init__(self, message=None, code=None):
        super().__init__(self.regex, message=message, code=code)


def validate_ums_student_email(value):
    try:
        CustomUMSStudentEmailValidator()(value)
    except ValidationError as e:
        raise ValidationError(
            _("Invalid UMS student email: %(value)s"),
            params={"value": value},
            code="invalid",
        )


class UMSUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(   email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class UMSUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    # is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # linkedin = models.URLField(blank=True)
    # instagram = models.URLField(blank=True)
    # semester = models.PositiveSmallIntegerField(
    #     validators=[MinValueValidator(1), MaxValueValidator(14)],
    #     blank=True
    # )
    angkatan = models.PositiveIntegerField(
        choices=[
            (2020, "2020"),
            (2021, "2021"),
            (2022, "2022"),
            (2023, "2023"),
            (2024, "2024"),
            (2025, "2025"),
        ],
        default=datetime.datetime.now().year,
    )

    objects = UMSUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "angkatan"]

    @property
    def nim(self):
        return self.email.split("@")[0]

    @property
    def koordinator(self):
        if self.is_superuser:
            return "Admin"
        current_year = f'{(datetime.datetime.now().year)}'
        try:
            return self.asisten_set.get(divisi="Koordinator", periode=current_year).praktikum
        except:
            return None
        return self.asisten_set.filter(divisi="Koordinator", periode=current_year).first().praktikum

    @property
    def asisten(self):
        if self.is_superuser:
            return True
        current_year = f'{(datetime.datetime.now().year)}'
        try:
            return self.asisten_set.get(periode=current_year)
        except:
            return None

    @property
    def praktikum(self):
        if self.is_superuser:
            return ""

        return self.asisten.praktikum if self.asisten else None

    def __str__(self):
        return f"{self.nim} {self.first_name}"
    
    @property
    def jabatan(self):
        if self.is_superuser:
            return "Admin"
        elif self.koordinator:
            return "Koordinator"
        elif self.asisten:
            return "Asisten"
        else:
            return "Peserta"

    def get_dict(self):
        user_data = {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "is_staff": self.is_staff,
            "is_verified": self.is_active,
            "is_superuser": self.is_superuser,
            "asisten": self.asisten,
            "koordinator": self.koordinator,
            "praktikum": self.praktikum,
            "nim": self.nim,
            "angkatan": self.angkatan,
            "jabatan": self.jabatan,
        }
        return user_data
