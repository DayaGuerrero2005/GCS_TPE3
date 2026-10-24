#!/bin/sh
# Prepara el contenedor antes de arrancar Django
set -e

echo "Esperando a PostgreSQL en ${POSTGRES_HOST:-localhost}:${POSTGRES_PORT:-5432}..."
python - <<'PY'
import os, time, psycopg2
for intento in range(30):
    try:
        psycopg2.connect(
            dbname=os.environ.get("POSTGRES_DB", "tareas"),
            user=os.environ.get("POSTGRES_USER", "tareas"),
            password=os.environ.get("POSTGRES_PASSWORD", "tareas"),
            host=os.environ.get("POSTGRES_HOST", "localhost"),
            port=os.environ.get("POSTGRES_PORT", "5432"),
        ).close()
        print("PostgreSQL disponible")
        break
    except psycopg2.OperationalError:
        time.sleep(2)
else:
    raise SystemExit("PostgreSQL no respondió a tiempo")
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
