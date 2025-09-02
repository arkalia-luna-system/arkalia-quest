
# 🔐 Authentification Docker - Guide de résolution des erreurs



## ❌ Erreur courante : "Cannot perform an interactive login from a non TTY device"


Cette erreur se produit quand Docker essaie de faire un login interactif dans un environnement non-TTY (CI/CD, scripts automatisés, etc.).


## ✅ Solutions



### 1. **Utiliser --password-stdin (Recommandé)**



```bash


# ✅ Correct - Utilise stdin pour le mot de passe

echo "votre_mot_de_passe" | docker login -u "votre_username" --password-stdin


# ❌ Incorrect - Peut causer des problèmes de TTY

docker login -u "votre_username" -p "votre_mot_de_passe"

```



### 2. **Script d'authentification sécurisé**


Utilisez le script fourni :


```bash


# Rendre le script exécutable

chmod +x scripts/docker-auth.sh


# Exécuter l'authentification

./scripts/docker-auth.sh

```



### 3. **Variables d'environnement**


Définissez vos credentials dans l'environnement :


```bash

export DOCKER_USERNAME="votre_username"
export DOCKER_PASSWORD="votre_mot_de_passe"


# Puis exécutez le script

./scripts/docker-auth.sh

```



### 4. **Fichier .env (pour le développement local)**


Créez un fichier `.env` à la racine du projet :


```bash


# .env

DOCKER_USERNAME=votre_username
DOCKER_PASSWORD=votre_mot_de_passe
DOCKER_REGISTRY=docker.io

```



## 🚀 Utilisation dans les scripts



### Script de déploiement principal



```bash


# Déploiement Docker local (sans authentification)

./scripts/deploy.sh docker


# Construction Docker uniquement

./scripts/deploy.sh docker-build

```



### Script de déploiement avancé



```bash


# Déploiement avec authentification

./scripts/deploiement/deploy.sh

```



## 🔍 Vérifications préalables


Avant d'exécuter les scripts, vérifiez que :

1. **Docker est installé** : `docker --version`
2. **Docker daemon fonctionne** : `docker info`
3. **Vous avez les permissions** : `docker ps`


## 🐳 Commandes Docker utiles



```bash


# Voir les images locales

docker images


# Voir les conteneurs en cours

docker ps


# Voir les logs d'un conteneur

docker logs arkalia-quest


# Arrêter un conteneur

docker stop arkalia-quest


# Supprimer un conteneur

docker rm arkalia-quest


# Nettoyer les images non utilisées

docker image prune

```



## 🚨 Dépannage



### Erreur : "permission denied"



```bash


# Ajouter votre utilisateur au groupe docker

sudo usermod -aG docker $USER


# Redémarrer la session ou exécuter

newgrp docker

```



### Erreur : "Cannot connect to the Docker daemon"



```bash


# Démarrer Docker

sudo systemctl start docker


# Vérifier le statut

sudo systemctl status docker

```



### Erreur : "authentication required"



```bash


# Vérifier que vous êtes connecté

docker login


# Ou utiliser le script sécurisé

./scripts/docker-auth.sh

```



## 📋 Workflow recommandé


1. **Développement local** : `./scripts/deploy.sh docker`
2. **Test de build** : `./scripts/deploy.sh docker-build`
3. **Authentification** : `./scripts/docker-auth.sh`
4. **Déploiement** : `./scripts/deploiement/deploy.sh`


## 🔒 Sécurité



- ⚠️ **Ne jamais commiter** le fichier `.env` avec des credentials


- ✅ **Utiliser** des variables d'environnement en production


- 🔐 **Rotater** régulièrement les mots de passe


- 📝 **Logger** les tentatives d'authentification
