# Étape 1 : Construire l'application Angular
FROM node:18 AS build

# Définir le répertoire de travail
WORKDIR /app

# Copier uniquement les fichiers package.json et package-lock.json
COPY package.json package-lock.json ./

# Installer les dépendances avec --legacy-peer-deps
RUN npm install --legacy-peer-deps

# Copier tout le code source après l’installation des dépendances
COPY . .

# Construire l'application Angular en mode production
RUN npm run build --configuration production --project=Angular7

# Étape 2 : Servir l'application avec Nginx
FROM nginx:alpine

# Définir le répertoire de travail
WORKDIR /usr/share/nginx/html

# Supprimer les fichiers HTML par défaut de Nginx
RUN rm -rf ./*

# Copier les fichiers générés depuis l'étape de build
COPY --from=build /app/dist/angular7 ./ 

# Copier le fichier de configuration Nginx (s'il existe)
COPY nginx.conf /etc/nginx/nginx.conf

# Exposer le port 80
EXPOSE 80

# Lancer Nginx
ENTRYPOINT ["nginx", "-g", "daemon off;"]
