# Dockerfile

ARG PYTHON_VERSION=3.11.10
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt
# RUN python manage.py collectstatic --noinput

# EXPOSE 8000

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_laboratorium.wsgi:application"]
CMD ["hypercorn", "--certfile", "./certs/letsencrypt/live/labtiums.web.id/fullchain.pem", "--keyfile", "./certs/letsencrypt/live/labtiums.web.id/privkey.pem","--bind", "0.0.0.0:8000", "--quic-bind", "0.0.0.0:8000", "--insecure-bind", "127.0.0.1:80", "web_laboratorium.wsgi:application"]
ENTRYPOINT ["./entrypoint.sh"]
