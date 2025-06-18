"""
WSGI config for DjangoProjectFinal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Configura el path para incluir el directorio del proyecto
project_root = Path(__file__).resolve().parent.parent
apps_path = os.path.join(project_root, 'aplicaciones')

# Añade los paths necesarios
paths = [
    str(project_root),
    apps_path,
    os.path.join(project_root, 'DjangoProjectFinal')
]

for path in paths:
    if path not in sys.path:
        sys.path.insert(0, path)

# Configura las variables de entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProjectFinal.settings')

# Importa y configura la aplicación WSGI
from django.core.wsgi import get_wsgi_application

# Asegúrate de que Django esté configurado correctamente
try:
    import django
    django.setup()
except Exception as e:
    print(f"Error al configurar Django: {e}")
    raise

# Crea la aplicación WSGI
application = get_wsgi_application()
