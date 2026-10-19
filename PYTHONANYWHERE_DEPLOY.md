# Guía Completa de Despliegue en PythonAnywhere
## Proyecto Supermercado PastelMarket

Esta guía detalla paso a paso el procedimiento exacto adaptado a la estructura de tu cuenta en **PythonAnywhere** (`ActividadDjango1`).

---

## 1. Solución Rápida al Error 400 (Bad Request)

El **Error 400** en Django ocurre cuando `DEBUG=False` y el dominio que accede a la web (en este caso `ActividadDjango1.pythonanywhere.com`) **no se encuentra listado en `ALLOWED_HOSTS`**.

### ¿Cómo solucionarlo?
1. `supermarket_project/settings.py` **no agrega comodines**: solo acepta los dominios declarados en el `.env`. Un comodín como `.pythonanywhere.com` aceptaría también las aplicaciones de otros usuarios de PythonAnywhere.
2. En tu archivo `.env` en PythonAnywhere (`/home/ActividadDjango1/desarrollo-seguro-10-09/.env`), declara exactamente tu dominio:
   ```env
   ALLOWED_HOSTS=actividaddjango1.pythonanywhere.com
   CSRF_TRUSTED_ORIGINS=https://actividaddjango1.pythonanywhere.com
   ```
3. `SECRET_KEY` es obligatoria y debe ser única por entorno. Genera una nueva con:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
   ```

---

## 2. Rutas Reales de tu Proyecto en PythonAnywhere

Al clonar el repositorio, la estructura queda directamente en la raíz de `desarrollo-seguro-10-09` (sin subcarpeta `django-project`):

- **Directorio Raíz del Proyecto**:
  ```
  /home/ActividadDjango1/desarrollo-seguro-10-09
  ```
- **Entorno Virtual**:
  ```
  /home/ActividadDjango1/desarrollo-seguro-10-09/venv
  ```
- **Directorio de Estáticos (`staticfiles`)**:
  ```
  /home/ActividadDjango1/desarrollo-seguro-10-09/staticfiles
  ```
- **Directorio de Multimedia (`media`)**:
  ```
  /home/ActividadDjango1/desarrollo-seguro-10-09/media
  ```

---

## 3. Configuración en la Pestaña "Web" de PythonAnywhere

En la pestaña **Web** de tu panel de PythonAnywhere, completa las secciones tal como se indica a continuación:

### A. Sección "Code"
- **Source code**:
  ```
  /home/ActividadDjango1/desarrollo-seguro-10-09
  ```
- **Working directory**:
  ```
  /home/ActividadDjango1/desarrollo-seguro-10-09
  ```
- **WSGI configuration file**:
  Haz clic en el enlace `/var/www/ActividadDjango1_pythonanywhere_com_wsgi.py`, borra todo su contenido y pega:
  ```python
  import os
  import sys
  from django.core.wsgi import get_wsgi_application

  path = os.path.expanduser("~/desarrollo-seguro-10-09")
  if path not in sys.path:
      sys.path.insert(0, path)

  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supermarket_project.settings")
  application = get_wsgi_application()
  ```
  *(Haz clic en el botón superior **Save**)*.

### B. Sección "Virtualenv"
- Ingresa la ruta:
  ```
  /home/ActividadDjango1/desarrollo-seguro-10-09/venv
  ```

### C. Sección "Static files" (Mapeos del PDF)
Asegúrate de tener exactamente dos filas de mapeo:

| URL | Directory |
|---|---|
| `/static/` | `/home/ActividadDjango1/desarrollo-seguro-10-09/staticfiles` |
| `/media/` | `/home/ActividadDjango1/desarrollo-seguro-10-09/media` |

---

## 4. Comandos de Actualización en la Terminal Bash

En la terminal de PythonAnywhere, ejecuta los siguientes comandos para sincronizar los cambios y aplicar archivos estáticos:

```bash
cd ~/desarrollo-seguro-10-09
git pull origin main

# Activar el entorno virtual si no está activo:
source venv/bin/activate

# Instalar o actualizar dependencias:
pip install -r requirements.txt

# Recopilar los archivos estáticos:
python manage.py collectstatic --noinput

# Aplicar migraciones y datos base:
python manage.py migrate
python init_data.py
```

---

## 5. Recargar y Probar

1. Vuelve a la pestaña **Web** de PythonAnywhere.
2. Haz clic en el botón verde superior: **"Reload ActividadDjango1.pythonanywhere.com"**.
3. Abre tu sitio:
   [https://ActividadDjango1.pythonanywhere.com/](https://ActividadDjango1.pythonanywhere.com/)
4. ¡El Error 400 habrá desaparecido y el sitio cargará con todos los estilos de Tailwind CSS y funciones completas!
