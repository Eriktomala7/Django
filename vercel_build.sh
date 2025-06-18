#!/bin/bash

# Configurar entorno
export PYTHONUNBUFFERED=1
export PYTHONPATH="/var/task/DjangoProjectFinal:/var/task/aplicaciones:$PYTHONPATH"

# Función para mostrar mensajes de error
error_exit() {
    echo "ERROR: $1" >&2
    exit 1
}

echo "=== Iniciando construcción en Vercel ==="

# 1. Instalar dependencias
echo "1. Instalando dependencias..."
pip install --upgrade pip || error_exit "Error actualizando pip"
pip install -r requirements.txt || error_exit "Error instalando dependencias"

# 2. Verificar instalación de Django
echo "2. Verificando instalación..."
python -c "import django; print(f'Django version: {django.__version__}')" || error_exit "Error al importar Django"

# 3. Aplicar migraciones
echo "3. Aplicando migraciones..."
python manage.py migrate --noinput || error_exit "Error aplicando migraciones"

# 4. Recolectar archivos estáticos
echo "4. Recolectando archivos estáticos..."
python manage.py collectstatic --noinput || error_exit "Error recolectando archivos estáticos"

# 5. Verificar que la aplicación WSGI se puede cargar
echo "5. Verificando configuración WSGI..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProjectFinal.settings')
try:
    from django.core.wsgi import get_wsgi_application
    app = get_wsgi_application()
    print('✅ WSGI configurado correctamente')
except Exception as e:
    print(f'❌ Error en la configuración WSGI: {str(e)}')
    raise
" || error_exit "Error en la configuración WSGI"

echo "✅ Construcción completada exitosamente"
