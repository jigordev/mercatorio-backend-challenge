#!/bin/bash

set -e

if [ "$RUN_MIGRATIONS" = "1" ]; then
    echo "Aplicando migrações..."
    uv run python manage.py migrate

    echo "Migrações aplicadas!"

    echo "Coletando arquivos estáticos"
    uv run python manage.py collectstatic --noinput

    echo "Verificando superusuário..."
    uv run python manage.py shell << EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superusuário '{username}' criado com sucesso.")
else:
    print(f"Superusuário '{username}' já existe.")
EOF

fi

echo "Iniciando aplicação..."
exec "$@"
