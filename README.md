# OpenStalk - Plateforme OSINT 🕵️‍♂️

OpenStalk est une plateforme d'investigation en sources ouvertes (OSINT) conçue par CART-Corporation. Elle a pour but d'assister les équipes de cybersécurité dans leurs campagnes d'investigation. La plateforme permet de centraliser la collecte, d'automatiser l'extraction d'entités (Emails, IP, Domaines) et d'assurer la traçabilité des preuves numériques collectées.

---

## ✨ Fonctionnalités Principales

* **Gestion des campagnes** : Création de dossiers d'enquête cloisonnés , suppression  et consultation de rapports de campagne.
* **Outils de collecte automatisés** : Connecteurs API (GitHub, Wikipedia) , collecte HTTP respectueuse avec pause entre les requêtes , et import de fichiers pour extraire des IPs et emails.
* **Tableau de bord interactif** : Visualisation des indicateurs clés tels que les artéfacts collectés, les entités détectées et les sources actives.
* **Conformité et sécurité** : Respect du cadre légal (Politique RGPD, transparence) , droit à l'oubli , journal d'audit complet , et authentification sécurisée avec stockage chiffré des mots de passe.

---

## ⚙️ Prérequis

Pour récupérer et exécuter ce projet, vous aurez besoin de :
* **GIT** 
* **Python** 
* Un compte **Github** 

---

## 🚀 Installation

**1. Récupération du projet** Ouvrez un terminal et clonez le dépôt avec la commande suivante:
`git clone https://github.com/clementbtt/Open-Stalk.git` 

**2. Installation des modules Python** Afin d'installer toutes les dépendances nécessaires, utilisez le fichier `requirements.txt` fourni:
`pip install -r requirements.txt` 

---

## 🔐 Paramétrage des variables d'environnement

Deux variables d'environnement doivent être paramétrées dans le fichier `app/.env`.

**1. Clé secrète Flask** (`FLASK_SECRET_KEY`)
Cette clé est utilisée par Flask pour chiffrer les données de session. Pour la générer, tapez ceci dans votre terminal :
`python -c 'import secrets; print(secrets.token_hex(32))'` 

**2. Clé d'API GitHub** (`GITHUB_KEY`)
Cette clé est utile pour le scraping. 
* Rendez-vous sur votre compte GitHub > **Settings**.
* Allez dans **Developer settings** > **Tokens (classic)**.
* Cliquez sur **Generate new token** > **classic**.
* Copiez la clé générée (attention, elle ne sera visible qu'une fois).

**Format du fichier `app/.env` :**
FLASK_SECRET_KEY=votre_cle_secrete_generee 
GITHUB_KEY=votre_token_github_classic 

---

## 💻 Lancement de l'application

1. Dans votre terminal, déplacez-vous dans le dossier `app`:
`cd app` 

2. Lancez le serveur de l'application Flask:
`flask --app server run` 

3. Ouvrez votre navigateur web et recherchez `localhost:5000`.
4. Lors de votre première connexion, cliquez sur **"S'inscrire ici"** pour créer votre compte.

---

## 🧪 Tests unitaires

Des tests unitaires sont présents dans le projet. Pour les exécuter :

1. Déplacez-vous dans le dossier `tests` depuis la racine du projet:
`cd ../tests` 

2. Lancez l'exécution avec la commande pytest:
`pytest` 

---

## Auteurs

* **Clément Boutet** _alias_ [@clementbtt](https://github.com/clementbtt)
* **Raphaël Loric _alias_ [@Mxrphee](https://github.com/Mxrphee)** 
* **Aïcha Sesay Lukumuena** 
* **Théo Zeimet _alias_ [@THZeimet](https://github.com/THZeimet)** 
