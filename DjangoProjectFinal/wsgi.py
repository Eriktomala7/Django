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

# Asegúrate de que el directorio de aplicaciones esté en el path
apps_path = os.path.join(project_root, 'aplicaciones')
if apps_path not in sys.path:
    sys.path.append(apps_path)

# Configura las variables de entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProjectFinal.settings')

# Inicializa la aplicación Django
from django.core.wsgi import get_wsgi_application

# Asegúrate de que las aplicaciones estén cargadas
import django
django.setup(set_prefix=False)

# Crea la aplicación WSGI
application = get_wsgi_application()
