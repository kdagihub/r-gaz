#!/bin/bash

# Attendre que la base de données soit prête
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started"

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Exécuter la commande passée au conteneur
exec "$@"