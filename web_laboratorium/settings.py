"""
Django settings for web_laboratorium project. 

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from pickle import NONE
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y6n8u_7*_#$&!peeg&088p4c1milhh)+61n7rh@p2k6=65e(+y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app", "localhost"]


# Application definition

INSTALLED_APPS = [
    'web_laboratorium.apps.app_main',
    'web_laboratorium.apps.app_auth',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web_laboratorium.apps.django_email_verification' 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web_laboratorium.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # os.path.join(BASE_DIR,'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'web_laboratorium.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

load_dotenv()

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.getenv("DB_DATABASE"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}




# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

AUTH_USER_MODEL = "app_auth.UMSUser"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles_build", "static")
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
PUBLIC_ROOT = os.path.join(MEDIA_ROOT, "public")
UPLOAD_ROOT = os.path.join(MEDIA_ROOT, "uploads")
UPLOAD_URL = "uploads/"
PUBLIC_URL = "public/"
PENDAFTARAN_URL = UPLOAD_URL + 'pendaftaran/'
PERSYARATAN_URL = UPLOAD_URL + "persyaratan/"
# PERSYARATAN_URL = PUBLIC_URL + "persyaratan"
# PERSYARATAN_PATH = os.path.join(PUBLIC_ROOT, "persyaratan")

LOGIN_URL = '/login/'

# EMAIL VERIFICATION SETTINGS

def email_verified_callback(user):
    user.is_verified = True


def password_change_callback(user, password):
    user.set_password(password)


# Global Package Settings
EMAIL_DESTINATION = os.getenv("EMAIL_DESTINATION", "")  # empty to not force all email to go to this address
EMAIL_FROM_ADDRESS = os.getenv("EMAIL_FROM_ADDRESS", "")  # mandatory
EMAIL_PAGE_DOMAIN = os.getenv("EMAIL_PAGE_DOMAIN", "http://localhost:8000/")  # mandatory (unless you use a custom link)
EMAIL_MULTI_USER = False  # optional (defaults to False)

# Email Verification Settings (mandatory for email sending)
EMAIL_MAIL_SUBJECT = "Confirm your email"
EMAIL_MAIL_HTML = "mail_body.html"
EMAIL_MAIL_PLAIN = "mail_body.txt"
EMAIL_MAIL_TOKEN_LIFE = 60 * 60  # one hour

# Email Verification Settings (mandatory for builtin view)
EMAIL_MAIL_PAGE_TEMPLATE = "email_success_template.html"
EMAIL_MAIL_CALLBACK = email_verified_callback

# Password Recovery Settings (mandatory for email sending)
EMAIL_PASSWORD_SUBJECT = "Change your password"
EMAIL_PASSWORD_HTML = "password_body.html"
EMAIL_PASSWORD_PLAIN = "password_body.txt"
EMAIL_PASSWORD_TOKEN_LIFE = 60 * 10  # 10 minutes

# Password Recovery Settings (mandatory for builtin view)
# EMAIL_PASSWORD_PAGE_TEMPLATE = "password_changed_template.html"
EMAIL_PASSWORD_CHANGE_PAGE_TEMPLATE = "password_change_template.html"
EMAIL_PASSWORD_CALLBACK = password_change_callback

# For Django Email Backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("SMTP_HOST", "")
EMAIL_PORT = int(os.getenv("SMTP_PORT", 0))
EMAIL_HOST_USER = os.getenv("SMTP_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("SMTP_HOST_PASSWORD", "")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
