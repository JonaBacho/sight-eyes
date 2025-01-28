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

# Variable globale pour stocker les informations de l'image active
active_image = {
    'id': None,
    'keyword': None,
    'url': None,
    'date_uploaded': None
}

filey = None

# Variable pour suivre l'état de l'utilisateur (en attente de sélection d'un ID)
user_state = {}

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

PROGRAM_PID = get_program_pid()

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
        global filey
        file_info = bot.get_file(received_message.photo[-1].file_id)
        file = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')
        filey = file.content
        
        connection = create_connection()
        if connection is None:
            bot.send_message(received_message.chat.id, "❌ Erreur de connexion à la base de données.")
            return

        # Demander un mot-clé pour l'image
        bot.send_message(received_message.chat.id, "🔑 Veuillez envoyer un mot-clé pour cette image.")
        user_state[received_message.chat.id] = {'waiting_for_key': True}


# Commande /search
@bot.message_handler(commands=['search'])
def list_images(message: Message):
    connection = create_connection()
    if connection is None:
        bot.send_message(message.chat.id, "❌ Impossible de se connecter à la base de données.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, image_url, keyword, date_uploaded FROM image")
        results = cursor.fetchall()

        if results:
            bot.send_message(message.chat.id, "🔍 Images disponibles :")
            for row in results:
                image_id = row[0]
                image_url = row[1]
                keyword = row[2]
                date_uploaded = row[3]
                
                image_path = os.path.join("..", image_url)  # Construire le chemin complet
                
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as img_file:
                        bot.send_photo(
                            message.chat.id,
                            img_file,
                            caption=f"ID: {image_id}\nMot-clé: {keyword}\nDate: {date_uploaded}"
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        f"⚠️ Image non trouvée sur le serveur.\nID: {image_id} | Mot-clé: {keyword} | Date: {date_uploaded}"
                    )

            cursor.close()
            connection.close()
            
            # Demander à l'utilisateur de choisir un ID
            bot.send_message(message.chat.id, "Veuillez choisir un ID d'image en répondant avec l'ID correspondant.")
            user_state[message.chat.id] = {'waiting_for_id': True}
            
        else:
            bot.send_message(message.chat.id, "⚠️ Aucune image disponible.")
    except Error as e:
        bot.send_message(message.chat.id, f"❌ Erreur lors de la recherche : {e}")
    finally:
        cursor.close()
        connection.close()

# Signaux inchangés...
# Commande pause, resume, cancel, bip

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


@bot.message_handler(content_types=['text'])
def handle_keyword(keyword_message: Message):
    global filey
    
    id_message = keyword_message
    
    if (not user_state.get(id_message.chat.id, {}).get('waiting_for_id')) and (not user_state.get(keyword_message.chat.id, {}).get('waiting_for_key')):
        bot.send_message(id_message.chat.id, "❌ Erreur : Nous n'attendions pas un message maintenant !\nConsultez /start")

    if user_state.get(keyword_message.chat.id, {}).get('waiting_for_key'):
        keyword = keyword_message.text.strip()
        connection = create_connection()
        if not keyword:
            bot.send_message(keyword_message.chat.id, "❌ Le mot-clé ne peut pas être vide.")
            return

        cursor = connection.cursor()
        try:
            # Enregistrer l'image dans le dossier "image"
            image_id = None
            cursor.execute("INSERT INTO image (image_url, keyword) VALUES (%s, %s)", ("", keyword))
            connection.commit()
            image_id = cursor.lastrowid
            
            
            image_name = f"{image_id}.jpg"
            image_path = f"../image/{image_name}"
            with open(image_path, 'wb') as img_file:
                img_file.write(filey)

            # Mettre à jour la colonne image_url
            relative_path = f"image/{image_name}"  # Chemin relatif depuis le dossier Telegram
            cursor.execute("UPDATE image SET image_url = %s WHERE id = %s", (relative_path, image_id))
            connection.commit()

            bot.send_message(
                keyword_message.chat.id,
                f"✅ Image enregistrée avec succès !\nChemin : {relative_path}\nMot-clé : {keyword}"
            )
            user_state[keyword_message.chat.id] = {'waiting_for_key': False}
        except Error as e:
            bot.send_message(keyword_message.chat.id, f"❌ Erreur lors de l'enregistrement : {e}")
        finally:
            cursor.close()
            connection.close()

    if user_state.get(id_message.chat.id, {}).get('waiting_for_id'):
        selected_id = id_message.text.strip()
        connection = create_connection()
        cursor = connection.cursor()

        try:
            selected_id = int(selected_id)
        except ValueError:
            bot.send_message(id_message.chat.id, "❌ Veuillez entrer un ID valide.")
            return

        # Vérifier si l'ID existe parmi les résultats de la recherche
        cursor.execute("SELECT id, image_url, keyword, date_uploaded FROM image WHERE id = %s", (selected_id,))
        selected_image = cursor.fetchone()

        if selected_image:
            # Stocker les informations de l'image dans la variable globale
            active_image['id'] = selected_image[0]
            active_image['keyword'] = selected_image[2]
            active_image['url'] = selected_image[1]
            active_image['date_uploaded'] = selected_image[3]

            image_path = os.path.join("..", active_image['url'])  # Construire le chemin complet
            
            if os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    bot.send_photo(
                        id_message.chat.id,
                        img_file,
                        caption=f"✅ Image sélectionnée !\nID: {active_image['id']}\nMot-clé: {active_image['keyword']}\nDate: {active_image['date_uploaded']}"
                    )
                with open("active_id.txt", "w") as active_file:
                    active_file.write(str(active_image['id']))
                with open("active_url.txt", "w") as active_url:
                    active_url.write(image_path)
                user_state[id_message.chat.id]['waiting_for_id'] = False  # Désactiver l'attente d'ID
        else:
            bot.send_message(id_message.chat.id, "❌ Aucune image trouvée avec cet ID.")


    

# Gestion des contenus inattendus
@bot.message_handler(func=lambda message: True, content_types=['sticker', 'animation', 'video', 'voice', 'video_note', 'audio', 'document', 'contact', 'location', 'poll', 'dice', 'game', 'venue'])
def handle_unexpected_content(message: Message):
    bot.send_message(
        message.chat.id,
        "❌ Erreur : Contenu inattendu ! Seuls les messages texte et les photos sont acceptés. 😊"
    )
    

# Lancement du bot
if __name__ == "__main__":
    print("🤖 Bot en cours d'exécution...")
    bot.polling()

