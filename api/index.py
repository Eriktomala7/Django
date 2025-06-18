from django.core.wsgi import get_wsgi_application
import os
import sys
from pathlib import Path

# Asegúrate de que el directorio del proyecto esté en el path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Configura las variables de entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProjectFinal.settings')

# Inicializa la aplicación Django
application = get_wsgi_()

def handler(event, context):
    from django.core.handlers.wsgi import WSGIHandler
    from django.core.handlers.wsgi import WSGIRequest
    from io import BytesIO
    import json
    import base64

    # Configura las variables de entorno necesarias
    os.environ["PYTHONUNBUFFERED"] = "1"
    
    # Crea un entorno de solicitud WSGI
    environ = {
        'REQUEST_METHOD': event.get('httpMethod', 'GET'),
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': event.get('queryStringParameters', '') or '',
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.url_scheme': 'https',
        'wsgi.input': BytesIO(json.dumps(event.get('body', '')).encode() if event.get('body') else b''),
        'wsgi.errors': sys.stderr,
        'wsgi.version': (1, 0),
        'wsgi.run_once': False,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
    }

    # Agrega las cabeceras HTTP
    if 'headers' in event:
        for key, value in event['headers'].items():
            key = 'HTTP_' + key.upper().replace('-', '_')
            environ[key] = value

    # Maneja las cookies si existen
    if 'cookies' in event:
        environ['HTTP_COOKIE'] = '; '.join(event['cookies'])

    # Ejecuta la aplicación Django
    response = WSGIHandler()(environ, lambda status, headers: None)
    
    # Prepara la respuesta
    response_body = b''.join(response.streaming_content if hasattr(response, 'streaming_content') else [response.content])
    
    return {
        'statusCode': response.status_code,
        'headers': dict(response.items()),
        'body': response_body.decode('utf-8')
    }
