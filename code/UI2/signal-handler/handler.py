import signal
import time
import sys
import os

# Variable globale pour suivre l'état du programme
program_state = "IDLE"

def save_program_pid():
    """Enregistrer le PID du programme dans un fichier"""
    try:
        pid = os.getpid()  # Récupère le PID du processus en cours
        with open("program_pid.txt", "w") as pid_file:
            pid_file.write(str(pid))  # Enregistre le PID dans le fichier
        print(f"✅ Le PID du programme a été enregistré dans program_pid.txt : {pid}")
    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement du PID : {e}")

def handle_start(signum, frame):
    """Démarrer le programme"""
    global program_state
    if program_state in ["IDLE", "PAUSED"]:
        program_state = "RUNNING"
        print("🚀 Programme démarré.")
    else:
        print("⚠️ Le programme est déjà en cours d'exécution.")

def handle_pause(signum, frame):
    """Mettre le programme en pause"""
    global program_state
    if program_state == "RUNNING":
        program_state = "PAUSED"
        print("⏸️ Programme mis en pause.")
    else:
        print("⚠️ Impossible de mettre en pause. État actuel :", program_state)

def handle_resume(signum, frame):
    """Reprendre le programme"""
    global program_state
    if program_state == "PAUSED":
        program_state = "RUNNING"
        print("▶️ Programme repris.")
    else:
        print("⚠️ Impossible de reprendre. État actuel :", program_state)

def handle_cancel(signum, frame):
    """Annuler le programme"""
    global program_state
    program_state = "IDLE"
    print("❌ Programme annulé. Retour à l'état initial.")

def handle_bip(signum, frame):
    """Effectuer un bip ou signal sonore"""
    print("🔔 BIP - Signal sonore activé.")

# Associer les signaux aux fonctions
signal.signal(signal.SIGUSR1, handle_start)  # Signal START
signal.signal(signal.SIGUSR2, handle_pause)  # Signal PAUSE
signal.signal(signal.SIGINT, handle_resume)  # Signal RESUME
signal.signal(signal.SIGTERM, handle_cancel)  # Signal CANCEL
signal.signal(signal.SIGALRM, handle_bip)    # Signal BIP

def main_loop():
    """Boucle principale du programme"""
    global program_state
    print("🔄 Programme en attente de signaux... (État : IDLE)")
    try:
        while True:
            if program_state == "RUNNING":
                print("🚀 Programme en cours d'exécution...")
                time.sleep(2)  # Simule un travail actif
            elif program_state == "PAUSED":
                print("⏸️ Programme en pause. En attente de reprise...")
                time.sleep(2)
            elif program_state == "IDLE":
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Programme terminé manuellement.")
        sys.exit(0)

if __name__ == "__main__":
    save_program_pid()  # Enregistre le PID dès le démarrage
    main_loop()
