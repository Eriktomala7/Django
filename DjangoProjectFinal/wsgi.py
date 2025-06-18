"""
WSGI config for DjangoProjectFinal project.
"""

import os
from django.core.wsgi import get_wsgi_application

# Configura el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProjectFinal.settings')

# Configura la aplicación WSGI
application = get_wsgi_application()
