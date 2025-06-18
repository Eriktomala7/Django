"""
WSGI config for DjangoProjectFinal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Asegúrate de que el directorio del proyecto esté en el path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Configura las variables de entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProjectFinal.settings')

# Inicializa la aplicación Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Asegúrate de que el directorio de la aplicación esté en el path
app_path = os.path.join(project_root, 'aplicaciones')
if app_path not in sys.path:
    sys.path.append(app_path)
