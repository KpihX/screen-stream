# Screen Stream Project 🖥️🌐

Screen Stream est un projet qui permet de partager et visualiser en temps réel le bureau d'un ordinateur à distance. Ce projet est divisé en deux composants principaux, le serveur et le client, avec une interface graphique pour le client (client_gui). La communication s'effectue sur un réseau local (par défaut), mais peut être configurée pour fonctionner à travers différents réseaux en ajustant les adresses IP dans les fichiers de configuration du serveur et du client.

## Fonctionnalités 🚀

- **Capture d'écran en temps réel :** Le serveur capture l'écran de l'ordinateur hôte et le transmet en continu au client.
- **Affichage dynamique :** Le client reçoit et affiche les captures d'écran, permettant ainsi de visualiser à distance l'activité de l'écran du serveur.
- **Adaptable à différents réseaux :** Possibilité de fonctionner sur des réseaux locaux ou étendus en modifiant les configurations IP.

## Prérequis 📋

- Python 3.6+
- Bibliothèques Python spécifiées dans `requirements.txt`

## Configuration Environnementale 🛠️

### Clonage du Projet

Commencez par cloner le projet sur votre machine locale :

```bash
git clone https://github.com/KpihX/screen_stream.git
cd screen_stream
```

### Création d'un Environnement Virtuel

Il est recommandé d'utiliser un environnement virtuel pour exécuter ce projet afin d'éviter tout conflit de dépendances.

#### Sous Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

#### Sous Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### Installation des Dépendances

Installez les dépendances nécessaires à l'aide de pip :

```bash
pip install -r requirements.txt
```

## Configuration du Projet 🔧

Avant de lancer le serveur et le client, assurez-vous de configurer les adresses IP dans les fichiers du serveur (`server.py`) et du client (`client.py`, `client_gui.py`) pour qu'ils correspondent à votre réseau. Par défaut, les adresses IP sont configurées pour fonctionner en local (`localhost` ou `127.0.0.1`).

## Lancement 🚀

### Serveur

Lancez le serveur en exécutant la commande suivante :

```bash
python server.py
```

### Client GUI

Pour lancer l'interface graphique du client, utilisez :

```bash
python client_gui.py
```

## Utilisation 🖱️

Après avoir lancé le serveur et le client GUI, le bureau de l'ordinateur serveur sera diffusé en temps réel sur l'interface du client GUI. Vous pouvez ajuster la taille de la fenêtre client pour adapter l'affichage à vos besoins.

## Contribution 🤝

Les contributions au projet sont les bienvenues ! N'hésitez pas à proposer des améliorations ou à corriger des bugs en soumettant des pull requests ou en ouvrant des issues.

## Auteur ✍️

- KpihX

---

N'hésitez pas à explorer le code et à l'expérimenter pour mieux comprendre le fonctionnement interne du projet Screen Stream. Bon codage !
