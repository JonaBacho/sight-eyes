import telebot
import mysql.connector
from mysql.connector import Error
import os
import signal
import requests
from telebot.types import Message

# Token Telegram
TOKEN = '7734765252:AAG1zYgVpKJZlMh5TWS1frHRYin0a6Fq3Z4'
bot = telebot.TeleBot(TOKEN)

# Lire le PID du programme principal depuis le fichier
def get_program_pid():
    try:
        with open("../signal-handler/program_pid.txt", "r") as pid_file:
            pid = int(pid_file.read().strip())
        return pid
    except FileNotFoundError:
        print("❌ Le fichier program_pid.txt n'a pas été trouvé.")
        return None
    except ValueError:
        print("❌ Le contenu de program_pid.txt n'est pas un PID valide.")
        return None

PROGRAM_PID = get_program_pid()  # Récupère le PID à partir du fichier

# Connexion à la base de données
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ImageDB',
            connection_timeout=180,
            autocommit=True
        )
        print("✅ Connexion à la base de données réussie.")
        return connection
    except Error as e:
        print(f"❌ Erreur de connexion : {e}")
        return None

# Commande /start
@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    help_text = (
        "👋 Bienvenue sur le bot de gestion d'images !\n"
        "📤 /upload - Envoyer une image dans la base de données.\n"
        "🔍 /search - Afficher les images disponibles.\n"
        "⏸️ /pause - Mettre en pause le programme principal.\n"
        "▶️ /resume - Reprendre le programme principal.\n"
        "❌ /cancel - Annuler la tâche en cours.\n"
        "🔔 /bip - Faire biper le programme principal.\n"
        "\n💡 Utilisez ces commandes pour interagir avec le système."
    )
    bot.send_message(message.chat.id, help_text)

# Commande /upload
@bot.message_handler(commands=['upload'])
def upload_image(message: Message):
    bot.send_message(message.chat.id, "📸 Veuillez envoyer une image à enregistrer.")

    @bot.message_handler(content_types=['photo'])
    def handle_image(received_message: Message):
        connection = create_connection()
        if connection is None:
            bot.send_message(received_message.chat.id, "❌ Erreur de connexion à la base de données.")
            return

        cursor = connection.cursor()
        file_info = bot.get_file(received_message.photo[-1].file_id)
        file = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')

        image_name = f"{received_message.photo[-1].file_id}.jpg"
        image_data = file.content

        try:
            cursor.execute("INSERT INTO images (image_name, image_data) VALUES (%s, %s)", (image_name, image_data))
            connection.commit()
            bot.send_message(received_message.chat.id, "✅ Image enregistrée avec succès !")
        except Error as e:
            bot.send_message(received_message.chat.id, f"❌ Erreur lors de l'enregistrement : {e}")
        finally:
            cursor.close()
            connection.close()

# Commande /search
@bot.message_handler(commands=['search'])
def list_images(message: Message):
    connection = create_connection()
    if connection is None:
        bot.send_message(message.chat.id, "❌ Impossible de se connecter à la base de données.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, date_uploaded FROM images")
        results = cursor.fetchall()

        if results:
            bot.send_message(message.chat.id, "🔍 Images disponibles :")
            for row in results:
                bot.send_message(message.chat.id, f"ID: {row[0]} | Date: {row[1]}")  # Afficher les images
            bot.send_message(message.chat.id, "✏️ Répondez avec l'ID de l'image pour l'utiliser.")
        else:
            bot.send_message(message.chat.id, "⚠️ Aucune image disponible.")
    except Error as e:
        bot.send_message(message.chat.id, f"❌ Erreur lors de la recherche : {e}")
    finally:
        cursor.close()
        connection.close()

# Gestion des signaux locaux
def send_signal_to_program(signal_type: int, message: Message, success_msg: str):
    if PROGRAM_PID is None:
        bot.send_message(message.chat.id, "❌ Le PID du programme principal est introuvable.")
        return

    try:
        os.kill(PROGRAM_PID, signal_type)
        bot.send_message(message.chat.id, success_msg)
    except ProcessLookupError:
        bot.send_message(message.chat.id, "❌ Le programme principal n'est pas actif.")
    except PermissionError:
        bot.send_message(message.chat.id, "❌ Permissions insuffisantes pour envoyer le signal.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erreur : {e}")

@bot.message_handler(commands=['pause'])
def pause_signal(message: Message):
    send_signal_to_program(signal_type=signal.SIGSTOP, message=message, success_msg="⏸️ Programme mis en pause.")

@bot.message_handler(commands=['resume'])
def resume_signal(message: Message):
    send_signal_to_program(signal_type=signal.SIGCONT, message=message, success_msg="▶️ Programme repris.")

@bot.message_handler(commands=['cancel'])
def cancel_signal(message: Message):
    send_signal_to_program(signal_type=signal.SIGTERM, message=message, success_msg="❌ Programme arrêté.")

@bot.message_handler(commands=['bip'])
def bip_signal(message: Message):
    send_signal_to_program(signal_type=signal.SIGUSR1, message=message, success_msg="🔔 Signal de bip envoyé.")

# Lancement du bot
if __name__ == "__main__":
    bot.polling()
