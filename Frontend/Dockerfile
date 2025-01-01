# FROM node:alpine

# WORKDIR /usr/src/app

# COPY . /usr/src/app

# RUN npm install -g @angular/cli

# RUN npm install

# CMD ["ng", "serve", "--host", "0.0.0.0"]

# Utilisation de l'image officielle Node.js 18.20.5 avec Alpine pour un conteneur léger
FROM node:18.20.5-alpine

# Définir le répertoire de travail dans le conteneur
WORKDIR /usr/src/app

# Copier le fichier package.json et package-lock.json pour installer les dépendances
COPY package*.json ./

# Installer les dépendances du projet Angular
RUN npm install

# Copier tout le code source dans le conteneur
COPY . .

# Installer Angular CLI globalement dans le conteneur
RUN npm install -g @angular/cli

# Exposer le port 4200 (port par défaut pour Angular)
EXPOSE 4200

# Lancer le serveur Angular (ng serve) sur le port 4200
CMD ["ng", "serve", "--host", "0.0.0.0"]
