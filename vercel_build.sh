#!/bin/bash

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate --noinput

# Crear superusuario (solo en desarrollo, en producción usa variables de entorno)
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'password') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "¡Construcción completada!"
