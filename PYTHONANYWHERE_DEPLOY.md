# Guía Completa de Despliegue en PythonAnywhere
## Proyecto Supermercado PastelMarket

Esta guía detalla paso a paso el procedimiento exacto para desplegar el proyecto Django en **PythonAnywhere**, cumpliendo al 100% con las especificaciones y capturas del instructivo en PDF.

---

## 1. Resumen de Requisitos Previos en el Proyecto

El proyecto ya cuenta con todos los ajustes requeridos por el instructivo del PDF:
- **`settings.py`**:
  - `STATIC_URL = "/static/"`
  - `STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")`
  - `STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]`
  - `MEDIA_URL = "/media/"`
  - `MEDIA_ROOT = os.path.join(BASE_DIR, "media")`
  - Configuración de seguridad con `django-environ`: `CSRF_TRUSTED_ORIGINS`, `SECURE_PROXY_SSL_HEADER`, `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`.
- **`urls.py`**:
  - Servido condicional de `MEDIA_URL` y `STATIC_URL` mediante `static(...)` cuando `settings.DEBUG` es `True`.
- **Archivos de despliegue**:
  - Directorio `media/` inicializado.
  - Plantilla `.env.example` para entorno de producción.
  - Script de ayuda `pythonanywhere_wsgi.py`.
  - Estilos CSS compilados de Tailwind listos para `collectstatic`.

---

## 2. Paso a Paso en PythonAnywhere

### Paso 1: Abrir consola Bash y clonar el repositorio
1. Inicia sesión en [PythonAnywhere](https://www.pythonanywhere.com/).
2. Ve a la pestaña **Consoles** y abre una nueva consola **Bash**.
3. Clona el repositorio desde GitHub:
   ```bash
   git clone https://github.com/xaviromf-boop/desarrollo-seguro-10-09.git
   cd desarrollo-seguro-10-09/django-project
   ```

---

### Paso 2: Crear el entorno virtual e instalar dependencias
1. En la consola Bash, crea el entorno virtual (por ejemplo, con Python 3.10):
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 emprendevirtual
   ```
   *(Si no tienes `virtualenvwrapper`, puedes usar `python3.10 -m venv venv && source venv/bin/activate`)*.

2. Con el entorno activado (verás `(emprendevirtual)` en la terminal), instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

### Paso 3: Configurar variables de entorno y codificación UTF-8
1. Ejecuta las variables de exportación de codificación (Páginas 3 y 4 del PDF):
   ```bash
   export LANG=C.UTF-8
   export LC_ALL=C.UTF-8
   export PYTHONIOENCODING=utf-8
   ```
   *(Opcional: puedes añadirlas a `~/.bashrc` para que se apliquen siempre).*

2. Crea el archivo `.env` a partir de la plantilla:
   ```bash
   cp .env.example .env
   nano .env
   ```

3. Modifica los siguientes valores según tu cuenta de PythonAnywhere:
   ```env
   SECRET_KEY=clave_secreta_super_segura_de_mas_de_50_caracteres_aleatorios_12345
   DEBUG=False
   ALLOWED_HOSTS=tu_usuario.pythonanywhere.com,localhost,127.0.0.1
   INTERNAL_IPS=127.0.0.1
   CSRF_TRUSTED_ORIGINS=https://tu_usuario.pythonanywhere.com
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   SECURE_HSTS_SECONDS=3600
   DATABASE_URL=sqlite:///db.sqlite3
   ```
   *(Presiona `Ctrl + O` y luego `Enter` para guardar; `Ctrl + X` para salir de nano)*.

4. Asegura los permisos del archivo `.env` (Página 3 del PDF):
   ```bash
   chmod 600 .env
   ```

---

### Paso 4: Migraciones, datos iniciales y archivos estáticos
1. Aplica las migraciones de base de datos:
   ```bash
   python manage.py migrate
   ```

2. Carga los datos semilla iniciales (crea el usuario `admin` con contraseña `admin`):
   ```bash
   python init_data.py
   ```

3. Recopila los archivos estáticos en `staticfiles` (Página 3 del PDF):
   ```bash
   python manage.py collectstatic --noinput
   ```

4. Ejecuta el verificador de seguridad de Django:
   ```bash
   python manage.py check --deploy
   ```

---

### Paso 5: Configurar la pestaña "Web" en PythonAnywhere
1. Ve a la pestaña **Web** de PythonAnywhere.
2. Si no has creado la aplicación web, pulsa en **"Add a new web app"**, selecciona **"Manual configuration"** y la versión de Python correspondiente (ej. Python 3.10).

3. En la sección **Code**:
   - **Source code**:
     ```
     /home/<tu_usuario>/desarrollo-seguro-10-09/django-project
     ```
   - **Working directory**:
     ```
     /home/<tu_usuario>/desarrollo-seguro-10-09/django-project
     ```
   - **WSGI configuration file**:
     Haz clic en el enlace `/var/www/<tu_usuario>_pythonanywhere_com_wsgi.py`, borra todo su contenido y pega lo siguiente (Página 4 del PDF):
     ```python
     import os
     import sys
     from django.core.wsgi import get_wsgi_application

     path = os.path.expanduser("~/desarrollo-seguro-10-09/django-project")
     if path not in sys.path:
         sys.path.insert(0, path)

     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supermarket_project.settings")
     application = get_wsgi_application()
     ```
     Guarda los cambios con el botón superior **Save**.

4. En la sección **Virtualenv**:
   - Ingresa la ruta a tu entorno virtual:
     ```
     /home/<tu_usuario>/.virtualenvs/emprendevirtual
     ```
     *(O la ruta donde creaste el entorno `venv`)*.

5. En la sección **Static files** (Mapeos estáticos de la Página 5 del PDF):
   Configura las siguientes dos rutas:
   - **Fila 1**:
     - **URL**: `/static/`
     - **Directory**: `/home/<tu_usuario>/desarrollo-seguro-10-09/django-project/staticfiles`
   - **Fila 2**:
     - **URL**: `/media/`
     - **Directory**: `/home/<tu_usuario>/desarrollo-seguro-10-09/django-project/media`

---

### Paso 6: Recargar y Probar el Sitio
1. Ve a la parte superior de la pestaña **Web** y haz clic en el botón verde grande:
   **"Reload <tu_usuario>.pythonanywhere.com"**.
2. Abre en tu navegador tu URL:
   `https://<tu_usuario>.pythonanywhere.com/`
3. Ingresa con:
   - **Usuario**: `admin`
   - **Contraseña**: `admin`
4. Comprueba que:
   - Los estilos de Tailwind CSS cargan con normalidad.
   - Las alertas y presupuestos en CLP se muestran correctamente.
   - La opción *"Sin precio"* y las categorías funcionan sin contratiempos.
   - Las exportaciones a CSV y WhatsApp operan al 100%.

---

### Paso 7 (Opcional): Uso de Base de Datos MySQL (Página 5 del PDF)
Si decides usar MySQL en PythonAnywhere en lugar de SQLite:
1. En la pestaña **Databases** de PythonAnywhere, asigna una contraseña de MySQL y crea una base de datos (ej. `tu_usuario$supermarket`).
2. En tu archivo `.env`, modifica la variable `DATABASE_URL`:
   ```env
   DATABASE_URL=mysql://tu_usuario:tu_password_mysql@tu_usuario.mysql.pythonanywhere-services.com/tu_usuario$supermarket
   ```
3. Ejecuta `python manage.py migrate` y `python init_data.py`.
4. Recarga la aplicación web desde la pestaña **Web**.
