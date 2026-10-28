#!/usr/bin/env bash
# Arranca la aplicación en local (http://127.0.0.1:8000) para la demostración.
# Si ya hay un servidor escuchando en ese puerto, solo lo avisa y abre el navegador.
set -euo pipefail

PROYECTO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST=127.0.0.1
PUERTO=8000
URL="http://$HOST:$PUERTO/"

if ss -ltn "sport = :$PUERTO" | grep -q LISTEN; then
  echo "El servidor ya está corriendo en $URL"
  xdg-open "$URL" >/dev/null 2>&1 || true
  exit 0
fi

cd "$PROYECTO"
[ -f .env ] || { echo "Falta el archivo .env en $PROYECTO"; exit 1; }
source venv/bin/activate
python manage.py migrate --noinput >/dev/null

echo "Iniciando la aplicación en $URL  (Ctrl+C para detenerla)"
( sleep 2 && xdg-open "$URL" >/dev/null 2>&1 ) &
exec python manage.py runserver "$HOST:$PUERTO"
