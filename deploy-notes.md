# Notas de despliegue simulado

Estas notas describen cómo se instala una versión del **Gestor de tareas** fuera del repositorio, tal como lo hace el job `deploy` del pipeline.

## Qué se despliega

- Imagen Docker `gestor-tareas:<versión>`, construida y probada por el job `build`.
- Base de datos PostgreSQL 16 en un contenedor aparte.
- La versión sigue el formato `0.1.<número de ejecución>-<commit>` en ramas de trabajo y `X.Y.Z` (archivo `VERSION`) en `main`, donde además se publica la release `vX.Y.Z`.

## Requisitos

- Docker Engine con el plugin Docker Compose v2.
- Puerto 8000 libre.

## Pasos

1. **Crear una carpeta externa al repositorio**

   ```bash
   mkdir -p /tmp/despliegue-externo && cd /tmp/despliegue-externo
   ```

2. **Descargar el proyecto y el paquete de la versión**

   ```bash
   git clone https://github.com/<usuario>/<repositorio>.git proyecto
   ```

   Desde la pestaña *Actions* (artefacto `imagen-docker-<versión>`) o desde la *Release* correspondiente se descargan:
   `gestor-tareas-<versión>.tar.gz`, `docker-compose.deploy.yml`, `env.example` y `VERSION`. (El archivo de variables va sin punto inicial porque los artefactos de GitHub omiten archivos ocultos.)

3. **Cargar la imagen en Docker**

   ```bash
   gunzip -c gestor-tareas-<versión>.tar.gz | docker load
   ```

4. **Configurar variables**

   ```bash
   cp env.example .env     # cambiar la contraseña y la clave secreta en un entorno real
   ```

5. **Levantar los contenedores**

   ```bash
   IMAGE_TAG=<versión> docker compose -f docker-compose.deploy.yml up -d
   IMAGE_TAG=<versión> docker compose -f docker-compose.deploy.yml ps
   ```

   Al arrancar, `entrypoint.sh` espera a PostgreSQL, aplica las migraciones y ejecuta `collectstatic` antes de iniciar Gunicorn.

6. **Validar**

   - Navegador: `http://localhost:8000/` debe mostrar el Gestor de tareas con la versión desplegada en la cabecera.
   - Salud: `http://localhost:8000/health/` debe responder `{"estado": "ok", "version": "<versión>", "base_de_datos": "postgresql"}`.

7. **Revertir a la versión anterior (rollback)**

   ```bash
   IMAGE_TAG=<versión-anterior> docker compose -f docker-compose.deploy.yml up -d
   ```

   Los datos se conservan porque viven en el volumen `datos_postgres`.

8. **Detener**

   ```bash
   docker compose -f docker-compose.deploy.yml down       # conserva datos
   docker compose -f docker-compose.deploy.yml down -v    # borra también el volumen
   ```

## Automatización

En el pipeline, los pasos 1 a 6 los ejecuta el job **Deploy - despliegue simulado** en `/tmp/despliegue-externo` del runner. La validación en navegador la hace Chromium (Playwright) y las capturas quedan en el artefacto `capturas-despliegue`. El resumen del despliegue aparece en la página de la ejecución.
