import subprocess
import time
import os
import sys

# Fonction pour lancer un programme en arrière-plan
def start_program(command):
    try:
        # Lancer le programme en arrière-plan
        subprocess.Popen(command, shell=True)
        print(f"✅ Programme lancé : {command}")
    except Exception as e:
        print(f"❌ Erreur lors du lancement de {command} : {e}")

# Fonction pour démarrer le gestionnaire de signaux
def start_signal_handler():
    print("🔄 Lancement du gestionnaire de signaux...")
    try:
        # Lance le gestionnaire de signaux (par exemple, signal_handler.py)
        subprocess.Popen(["python3", "signal_handler.py"], shell=False)
        print("✅ Gestionnaire de signaux lancé avec succès.")
    except Exception as e:
        print(f"❌ Erreur lors du lancement du gestionnaire de signaux : {e}")

# Fonction pour démarrer le backend, le frontend et le bot Telegram
def start_backend_frontend_bot():
    print("⏳ Attente de 5 secondes avant de démarrer le backend, le frontend et le bot...")
    time.sleep(5)  # Attente de 5 secondes avant de démarrer les services

    # Démarrer le backend Node.js (remplacez par le chemin correct de votre script backend)
    start_program("node ../Web/backend/server.js")  # Remplacez le chemin vers votre dossier backend

    # Démarrer le frontend React (assurez-vous d'être dans le bon dossier)
    start_program("npm start --prefix ../Web/frontend")  # Remplacez le chemin vers votre dossier frontend

    # Démarrer le bot Telegram
    start_program("python3 ../Telegram/bot.py")  # Remplacez par le chemin de votre bot Telegram

def main():
    # Lancer le gestionnaire de signaux en premier
    start_signal_handler()

    # Attendre 5 secondes, puis démarrer le backend, frontend et bot
    start_backend_frontend_bot()

if __name__ == "__main__":
    main()
