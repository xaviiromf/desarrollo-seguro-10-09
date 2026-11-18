# Supermercado: listas de compras (Django)

CRUD de listas de compras con productos, cantidades y precios en CLP. Cada usuario ve solo sus propias listas.

- Producción: https://actividaddjango1.pythonanywhere.com
- Guía de despliegue: `PYTHONANYWHERE_DEPLOY.md`
- Entrega de la Evaluación U2 (Desarrollo Seguro): `evaluacion_u2/`

## Ejecutar en local

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # genera una SECRET_KEY propia (ver el comentario del archivo)
python manage.py migrate
python manage.py test shopping
python manage.py runserver
```

## Checklist de 5 minutos antes de cada push

1. **¿Hay secretos en el diff?** Revisa `git diff --staged` en busca de `SECRET_KEY`, contraseñas o tokens. El `.env` nunca se sube.
2. **¿La configuración de despliegue está bien?** Ejecuta `python manage.py check --deploy` con las variables de producción.
3. **¿Las pruebas están en verde?** Ejecuta `python manage.py test shopping`.
4. **¿El `.env` sigue fuera de git?** `git ls-files | grep -x .env` no debe devolver nada.

Si encuentras un secreto ya subido, no basta con borrarlo: hay que rotarlo.

## Laboratorio con Docker (Evaluación 3)

El laboratorio levanta el CRUD con un perfil diferenciado (`DEBUG=False`, `ALLOWED_HOSTS` acotado y secretos por variables de entorno) y lo publica **solo en la interfaz local**: http://127.0.0.1:8000. OWASP ZAP analiza esta instancia, nunca el despliegue público.

### Requisitos
- Docker 24 o superior con Docker Compose v2 (probado con Docker 29.9.2 y Compose 5.6.1).
- Opcional, para el análisis: OWASP ZAP Desktop 2.17.0 en el equipo anfitrión.

### Construir y levantar
```bash
cp .env.lab.example .env.lab        # y reemplaza SECRET_KEY y las contraseñas de prueba
docker compose build
docker compose up -d
docker compose ps                   # el servicio web debe quedar "healthy"
```
Las migraciones se aplican solas al arrancar (`docker/entrypoint.sh`). Para ejecutarlas a mano: `docker compose exec web python manage.py migrate`.

### Cuentas de prueba
```bash
docker compose exec web python manage.py crear_cuentas_prueba
```
Crea `qa_ana` y `qa_beto`, cada una con una lista ficticia. Sus contraseñas son las de `LAB_PASSWORD_ANA` y `LAB_PASSWORD_BETO` en `.env.lab`. Para un administrador: `docker compose exec web python manage.py createsuperuser`.

### Acceso y pruebas
- Aplicación: http://127.0.0.1:8000 (redirige al login).
- Pruebas automatizadas (en el entorno local): `python manage.py test shopping`.
- Detener: `docker compose down`. Borrar también la base del laboratorio: `docker compose down -v`.

### Seguridad del contenedor
- Imagen oficial `python:3.12-slim`, dependencias con versiones fijas y servidor **gunicorn** con **WhiteNoise** para los estáticos.
- Proceso con usuario sin privilegios (`app`, uid 10001), sistema de archivos de solo lectura, `no-new-privileges` y sin capacidades de Linux.
- La base SQLite del laboratorio vive en el volumen `lab_data`. `.dockerignore` deja fuera `.env*`, bases de datos, entornos virtuales y archivos ajenos a la construcción.
- Las cookies `Secure` y la redirección HTTPS están desactivadas **solo** porque el laboratorio usa HTTP. En producción (`.env` de PythonAnywhere) van activadas.
