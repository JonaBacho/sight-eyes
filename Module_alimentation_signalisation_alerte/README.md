# Module Alimentation, Signalisation et Alerte

## Objectif
Dans ce module, il est question de planifier l'alimentation des composants en besoin d'énergie et d'envoyer des alertes lorsque l'on trouve l'objet recherché.

## Matériels utilisés
Pour ce module, nous avons utilisé:
-   Un **buzzer** pour l'alerte sonore;
-   Des **LED** pour l'alerte visuelle;
-   Des **résistances de 10 KiloOhms et de 220 Ohms**;
-   Des **fils conducteurs**;
-   Un **ESP32-CAM** dont nous avons juste utilisé le volet **Wifi** pour des communications avec l'application utilisateur.

##  Actions menées
Au cours des deux semaines de prises en main, nous avons effectué:
-   **La réalisation d'un montage de contrôle de buzzer à partir d'un signal entrant** : Ce montage comprend une fonction qui pourra être déclenchée par les autres modules pour la signalisation;
-   **La coordination de la signalisation visuelle à la signalisation sonore**;
-   **La connexion de l'ESP32-CAM à un WiFi distant**: Cette partie à été effectuée pour pouvoir communiquer via Internet avec l'ESP32-CAM avec le module application.
-   **Le plan d'alimentation du robot**: L'alimentation source est une batterie. Néanmoins, il avait été prévu que cette batterie soit rechargeable par énergie solaire. Néanmoins nous n'avons pas encore effectué de tests physiques sur ce volet. Mais nous savons que nous aurons besoin d'**une plaque solaire**, d'un **adaptateur de tension**, d'un **circuit de charge (Powerboost 100)** et d'une **batterie rechargeable**.
Hors mis le volet solaire, il a été établi vu les besoins en énergie des autres modules que la battérie centrale devra pour renvoyer en sortie 12V. Cette énergie sera envoyée au module de contrôle des roues qui à son tour enverra de l'énergie à la carte de contrôle (Arduino pour les tests) qui à son tour alimentera les autres modules (Rasberry pi, ESP32-CAM). 

## Difficultés rencontrées
Nous avons rencontré des difficultés pour le téleversement des codes sur l'ESP32-CAM. Ce problème a été résolu mais la réussite du processus de téléversement d'un code sur ce matériel reste aléatoire.