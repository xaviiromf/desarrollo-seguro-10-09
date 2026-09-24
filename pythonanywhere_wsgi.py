"""
Configuración de WSGI para PythonAnywhere
==========================================
Copia y pega este contenido en el archivo de configuración WSGI de PythonAnywhere:
/var/www/<tu_usuario>_pythonanywhere_com_wsgi.py

(Asegúrate de ajustar la ruta al directorio donde clonaste tu proyecto en PythonAnywhere)
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Ruta al directorio raíz de tu proyecto Django en PythonAnywhere:
path = os.path.expanduser("~/desarrollo-seguro-10-09")
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supermarket_project.settings")

application = get_wsgi_application()
