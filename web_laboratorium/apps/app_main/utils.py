import mimetypes
from threading import Thread

from django.conf import settings
from django.template import Context, Template
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from web_laboratorium.apps.app_main.loa import loa_attatchment

def send_email_thread(
    targets, subject, text_path, html_path=None, context=None, attachments=None
):
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
    if attachments:
        for attatchment in attachments:
            mail.attach(*attatchment)
    mail.send()


def send_email(
    targets,
    subject,
    html_path=None,
    context=None,
    thread=True,
    text_path=None,
    attachments=None,
):
    if thread:
        t = Thread(
            target=send_email_thread,
            args=(targets, subject, text_path, html_path, context, attachments),
        )
        t.start()
    else:
        send_email_thread(targets, subject, text_path, html_path, context, attachments)


def send_status_email(user, pendaftaran, newStatus, thread=True):
    subject = "Status Pendaftaran Praktikum"
    context = {
        "nama": user.first_name,
        "praktikum": pendaftaran.praktikum.praktikum_name,
        "status": newStatus,
    }
    send_email([user.email], subject, "email/status_email.html", context, thread)


def extension_to_mime(extension):
    if not extension.startswith("."):
        extension = f".{extension}"
    if extension == ".webp":
        return "image/webp"

    mime_type, _ = mimetypes.guess_type(f"file{extension}")

    return mime_type
