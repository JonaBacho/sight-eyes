# Objectif

Développer et assembler un robot basé sur le châssis Keyestudio 4WD Mecanum Wheel capable de détecter, localiser et se déplacer vers des objets spécifiques grâce à l'intégration d'une caméra ESP32-CAM et de capteurs ultrasoniques.
Matériels utilisés

    Châssis Keyestudio 4WD Mecanum (avec roues omnidirectionnelles).
    Arduino UNO : Carte de contrôle principale.
    Carte L298N : Module de commande des moteurs.
    ESP32-CAM : Module caméra avec connectivité Wi-Fi.
    Capteur ultrasonique : Pour détection d’obstacles.
    Servomoteur : Permettant la rotation de la caméra et du capteur.
    Support batterie 18650 : Source d’alimentation.
    Visserie et câblage : Pour montage et connexions.
    Logiciels : Arduino IDE pour la programmation.

# Actions menées

    Montage physique du robot
        Installation des moteurs DC et des roues Mecanum.
        Fixation de la caméra ESP32-CAM et du capteur ultrasonique sur un servomoteur rotatif.
        Assemblage des cartes Arduino et L298N avec le câblage correspondant.

    Implémentation des fonctionnalités
        Programmation des fonctions de base : déplacement (avancer, tourner, s’arrêter).
        Test du streaming vidéo avec l’ESP32-CAM.
        Calibration du capteur ultrasonique pour détecter les obstacles.

    Tests unitaires
        Vérification individuelle des moteurs, capteurs, et caméra.
        Simulation des scénarios de détection et de déplacement vers un objet cible.

    Optimisation du circuit électrique
        Garantie d’une alimentation stable et suffisante pour tous les composants.

# Difficultés rencontrées

    Problème : Contrôle simultané des quatre roues avec la carte L298N.
        Solution : Couplage logique des roues opposées pour réduire le nombre de connexions nécessaires.

    Problème : Instabilité de l’alimentation pour l’ESP32-CAM lors des tests.
        Solution : Utilisation de batteries 18650 à capacité élevée et optimisation du câblage.

    Problème : Synchronisation des mouvements du servomoteur avec la caméra et le capteur.
        Solution : Ajout d’un délai dans le code pour coordonner les rotations.