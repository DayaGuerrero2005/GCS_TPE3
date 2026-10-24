# Gestor de tareas - Flujo CI/CD para Django

Aplicación Django con PostgreSQL usada para la práctica de **Gestión de la Configuración de Software** (UNEMI): integración continua con GitHub Actions, construcción de imágenes Docker y despliegue simulado.

## Estructura

```
manage.py
project/            configuración de Django
app/                app de tareas (modelo, vistas, plantillas, pruebas)
requirements.txt
Dockerfile          imagen basada en python:3.10
entrypoint.sh       espera a PostgreSQL, migra y arranca Gunicorn
docker-compose.yml          entorno de desarrollo (Django + PostgreSQL)
docker-compose.deploy.yml   despliegue con la imagen ya construida
scripts/capturar.py         validación en navegador (Playwright)
deploy-notes.md             pasos del despliegue simulado
.github/workflows/ci.yml    pipeline CI/CD
```

## Ejecutar en local

```bash
docker compose up --build
```

Abrir `http://localhost:8000/`.

## Pruebas sin Docker

```bash
pip install -r requirements.txt
python manage.py test
```

Requiere un PostgreSQL accesible; las credenciales se leen de `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST` y `POSTGRES_PORT`.

## Pipeline

| Job | Qué hace |
|---|---|
| CI - pruebas y análisis | flake8, `manage.py check`, verificación de migraciones y `manage.py test` contra PostgreSQL |
| Build - imagen Docker | construye y versiona la imagen, la valida con Compose, la etiqueta para Docker Hub (simulado) y la guarda como artefacto |
| Deploy - despliegue simulado | descarga proyecto e imagen en una carpeta externa, levanta con Compose y valida en navegador |
| Release - publicar versión | al integrar en `main` crea la etiqueta `v` + contenido de `VERSION` y publica la release con la imagen y las capturas |
