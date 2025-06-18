"""
WSGI config for DjangoProjectFinal project.
"""

import os
import sys
from pathlib import Path

# Configura los paths necesarios
project_root = Path(__file__).resolve().parent.parent
apps_path = os.path.join(project_root, 'aplicaciones')

# Añade los paths al sistema
for path in [str(project_root), apps_path, os.path.join(project_root, 'DjangoProjectFinal')]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Configura el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProjectFinal.settings')

# Configura la aplicación WSGI
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("WSGI configurado correctamente")
except Exception as e:
    print(f"Error en la configuración WSGI: {str(e)}")
    raise
