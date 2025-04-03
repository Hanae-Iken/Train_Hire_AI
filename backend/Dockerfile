# Étape 1 : Utiliser une image Python optimisée
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt ./

# Installer les dépendances (avec optimisation)
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code du backend
COPY . .

# Exposer le port utilisé par Django (8000)
EXPOSE 8000

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Appliquer les migrations de la base de données
RUN python manage.py migrate --noinput

# Lancer le serveur Django avec Gunicorn
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "Train_Hire_AI.wsgi:application"]