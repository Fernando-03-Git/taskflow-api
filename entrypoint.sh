#!/bin/sh
set -e

echo "Aplicando migraciones..."
alembic upgrade head

echo "Arrancando la API..."
exec uvicorn main:app --host 0.0.0.0 --port 8000