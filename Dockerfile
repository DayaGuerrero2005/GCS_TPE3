# Imagen base pedida por la guía
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# Primero solo requirements.txt: si no cambia, Docker reutiliza esta capa en el siguiente build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# El pipeline pasa la versión del build; queda visible en la página y en /health/
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}

RUN chmod +x /code/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/code/entrypoint.sh"]
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
