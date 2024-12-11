# Créer un fichier de service systemd
sudo nano /etc/systemd/system/start_daemon.service

# Contenu à ajouter dans ce fichier
[Unit]
Description=Lancement du démon pour start_daemon.py
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /chemin/vers/start_daemon.py
Restart=always
User=pi
WorkingDirectory=/chemin/vers/le/dossier/de/votre/script
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target

# Recharger systemd pour prendre en compte le nouveau service
sudo systemctl daemon-reload

# Activer le service au démarrage
sudo systemctl enable start_daemon.service

# Démarrer le service immédiatement
sudo systemctl start start_daemon.service

# Vérifier l'état du service
sudo systemctl status start_daemon.service
