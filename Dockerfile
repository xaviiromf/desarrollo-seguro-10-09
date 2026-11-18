# Imagen oficial de Python, misma serie (3.12) que el despliegue en PythonAnywhere.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Usuario sin privilegios; solo /data (base SQLite del laboratorio) es escribible por él.
RUN useradd --system --uid 10001 --no-create-home app \
    && mkdir -p /data && chown app:app /data

# Dependencias primero para aprovechar la caché de capas.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Solo el código de la aplicación, de forma explícita (nada de COPY . .), como propiedad de root:
# el proceso no puede modificarlo y ningún archivo ajeno o secreto entra a la imagen.
COPY manage.py ./
COPY supermarket_project/ supermarket_project/
COPY shopping/ shopping/
COPY theme/ theme/
COPY templates/ templates/
COPY static/ static/
COPY docker/ docker/

# Estáticos recopilados en la construcción; la clave es solo un marcador para este paso.
RUN SECRET_KEY=solo-para-collectstatic DEBUG=False python manage.py collectstatic --noinput

USER app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/login/', timeout=4)"

ENTRYPOINT ["/app/docker/entrypoint.sh"]
