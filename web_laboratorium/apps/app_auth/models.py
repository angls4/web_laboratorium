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
        extra_fields.setdefault("is_staff", True)
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
    REQUIRED_FIELDS = ["first_name", "linkedin", "instagram", "angkatan"]

    def __str__(self):
        nim = self.email.split("@")[0]
        return f"{nim} {self.first_name}"
