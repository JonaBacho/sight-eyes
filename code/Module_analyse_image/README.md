# Module d'Analyse d'Image pour Robot Suiveur d'Objet

## Introduction

Dans le cadre des systèmes robotiques modernes, la capacité à détecter et suivre un objet en temps réel est cruciale pour de nombreuses applications telles que la surveillance, la navigation autonome, ou encore l'interaction homme-machine. Ce module propose une solution complète pour un **robot suiveur d'objet** utilisant l'analyse d'image et l'intelligence artificielle. 

L'objectif de ce module est d'entraîner un modèle d'apprentissage automatique capable de reconnaître un objet spécifique, de le détecter dans un flux vidéo en temps réel et d'ajuster la position de la caméra pour maintenir l'objet centré dans l'image. Ce système est conçu pour être intégré dans des environnements contraints, tels qu'un **Raspberry Pi 3** équipé d'une caméra ESP32-CAM.

## Fonctionnalités Principales

1. **Entraînement d'un modèle TensorFlow Lite** : 
   - Création d'un modèle d'apprentissage basé sur une banque d'images spécifique à l'objet cible.
   - Conversion du modèle en un format optimisé pour les appareils embarqués.

2. **Détection en temps réel** :
   - Intégration du modèle TensorFlow Lite dans un algorithme de vision par ordinateur pour la détection d'objet dans un flux vidéo.

3. **Exécution sur Raspberry Pi 3** :
   - Optimisation des performances pour un environnement matériel limité.

4. **Connexion avec ESP32-CAM** :
   - Modification du pipeline vidéo pour utiliser l'ESP32-CAM comme source vidéo au lieu de la webcam classique.

5. **Suivi en temps réel avec servo-moteur** :
   - Ajout d'un système de suivi dynamique permettant de centrer l'objet détecté dans le cadre en ajustant la position de la caméra.

---

## Démonstration

![Demo GIF 1](path/to/demo1.gif)  
*Détection d'objet sur un flux vidéo standard.*

![Demo GIF 2](path/to/demo2.gif)  
*Suivi de l'objet avec caméra ESP32-CAM.*

---

## Installation et Utilisation

### Prérequis

- **Matériel** :
  - Raspberry Pi 3
  - ESP32-CAM
  - Servo-moteur compatible
- **Logiciels** :
  - TensorFlow Lite
  - OpenCV

### Étapes d'Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/JonaBacho/sight-eyes.git
   cd sight-eyes/code/Module_analyse_image
   ```

2. Installez les dépendances Python (après avoir activé votre environnement virtuel):
   ```bash
   pip install -r requirements.txt
   ```

3. Configurez le Raspberry Pi et l'ESP32-CAM en suivant les instructions du fichier : à completer

4. Démarrez la détection en temps réel :

   ```bash
   python3 object_detection_app.py
   ```
   
---

##  Architecture du fonctionnement interne du module
schema à faire
avec une description similaire à ce qui suit:
1. **Préparation des données** : Banque d'images et étiquetage.
2. **Entraînement du modèle TensorFlow Lite** : Script Python pour entraînement et conversion.
3. **Détection en temps réel** : Algorithme basé sur OpenCV et TensorFlow Lite.
4. **Intégration avec ESP32-CAM** : Flux vidéo via Wi-Fi.
5. **Contrôle des servo-moteurs** : Ajustement dynamique de la caméra pour suivre l'objet.

---

## Lien utile
Articles et Ressources Consultés
- **Entraînement TensorFlow Lite** :
Lien vers l'article
Un guide détaillé sur la création et la conversion de modèles pour appareils embarqués.

- **Utilisation d'ESP32-CAM** :
Lien vers l'article
Configuration de l'ESP32-CAM pour un flux vidéo en temps réel.

- **Contrôle des Servo-moteurs** :
Lien vers l'article
Tutoriel pour piloter un servo-moteur avec Python.
# Module d'Analyse d'Image pour Robot Suiveur d'Objet

## Introduction

Dans le cadre des systèmes robotiques modernes, la capacité à détecter et suivre un objet en temps réel est cruciale pour de nombreuses applications telles que la surveillance, la navigation autonome, ou encore l'interaction homme-machine. Ce module propose une solution complète pour un **robot suiveur d'objet** utilisant l'analyse d'image et l'intelligence artificielle. 

L'objectif de ce module est d'entraîner un modèle d'apprentissage automatique capable de reconnaître un objet spécifique, de le détecter dans un flux vidéo en temps réel et d'ajuster la position de la caméra pour maintenir l'objet centré dans l'image. Ce système est conçu pour être intégré dans des environnements contraints, tels qu'un **Raspberry Pi 3** équipé d'une caméra ESP32-CAM.

## Fonctionnalités Principales

1. **Entraînement d'un modèle TensorFlow Lite** : 
   - Création d'un modèle d'apprentissage basé sur une banque d'images spécifique à l'objet cible.
   - Conversion du modèle en un format optimisé pour les appareils embarqués.

2. **Détection en temps réel** :
   - Intégration du modèle TensorFlow Lite dans un algorithme de vision par ordinateur pour la détection d'objet dans un flux vidéo.

3. **Exécution sur Raspberry Pi 3** :
   - Optimisation des performances pour un environnement matériel limité.

4. **Connexion avec ESP32-CAM** :
   - Modification du pipeline vidéo pour utiliser l'ESP32-CAM comme source vidéo au lieu de la webcam classique.

5. **Suivi en temps réel avec servo-moteur** :
   - Ajout d'un système de suivi dynamique permettant de centrer l'objet détecté dans le cadre en ajustant la position de la caméra.

---

## Démonstration

![Demo GIF 1](path/to/demo1.gif)  
*Détection d'objet sur un flux vidéo standard.*

![Demo GIF 2](path/to/demo2.gif)  
*Suivi de l'objet avec caméra ESP32-CAM.*

---

## Installation et Utilisation

### Prérequis

- **Matériel** :
  - Raspberry Pi 3
  - ESP32-CAM
  - Servo-moteur compatible
- **Logiciels** :
  - TensorFlow Lite
  - OpenCV

### Étapes d'Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/JonaBacho/sight-eyes.git
   cd sight-eyes/code/Module_analyse_image
2. Installez les dépendances Python (après avoir activé votre environnement virtuel):
   ```bash
   pip install -r requirements.txt
3. Configurez le Raspberry Pi et l'ESP32-CAM en suivant les instructions du fichier : à completer
4. Démarrez la détection en temps réel :
   ```bash
   python3 object_detection_app.py
   
---

##  Architecture du fonctionnement interne du module
schema à faire
avec une description similaire à ce qui suit:
1. **Préparation des données** : Banque d'images et étiquetage.
2. **Entraînement du modèle TensorFlow Lite** : Script Python pour entraînement et conversion.
3. **Détection en temps réel** : Algorithme basé sur OpenCV et TensorFlow Lite.
4. **Intégration avec ESP32-CAM** : Flux vidéo via Wi-Fi.
5. **Contrôle des servo-moteurs** : Ajustement dynamique de la caméra pour suivre l'objet.

---

## Lien utile
Articles et Ressources Consultés
- **Entraînement TensorFlow Lite** :
Lien vers l'article
Un guide détaillé sur la création et la conversion de modèles pour appareils embarqués.

- **Utilisation d'ESP32-CAM** :
Lien vers l'article
Configuration de l'ESP32-CAM pour un flux vidéo en temps réel.

- **Contrôle des Servo-moteurs** :
Lien vers l'article
Tutoriel pour piloter un servo-moteur avec Python.
