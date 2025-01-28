import telebot
import mysql.connector
from mysql.connector import Error
import requests

# Token Telegram
TOKEN = '7734765252:AAG1zYgVpKJZlMh5TWS1frHRYin0a6Fq3Z4'
bot = telebot.TeleBot(TOKEN)

# Adresse IP de l'ESP32-CAM
ESP32_URL = "http://192.168.24.77"

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
        if connection.is_connected():
            print("✅ Connexion à la base de données réussie.")
            return connection
        else:
            print("❌ La connexion à la base de données a échoué.")
            return None
    except Error as e:
        print(f"Erreur lors de la tentative de connexion : {e}")
        return None

# Commande /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    help_text = (
        "👋 Bienvenue sur le bot de gestion d'images !\n"
        "📤 /upload - Envoyer une image dans la base de données.\n"
        "🔍 /search - Afficher les images uploadées et en choisir une.\n"
        "⏸️ /pause - Mettre en pause la recherche.\n"
        "▶️ /resume - Reprendre la recherche.\n"
        "❌ /cancel - Annuler la recherche en cours.\n"
        "\n💡 Utilisez ces commandes pour gérer vos images et interagir avec le robot."
    )
    bot.send_message(message.chat.id, help_text)

# Commande /upload
@bot.message_handler(commands=['upload'])
def upload_image(message):
    bot.send_message(message.chat.id, "Veuillez envoyer une image.")

    @bot.message_handler(content_types=['photo'])
    def handle_image(received_message):
        connection = create_connection()
        cursor = connection.cursor()

        file_info = bot.get_file(received_message.photo[-1].file_id)
        file = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')
        
        image_name = f"{received_message.photo[-1].file_id}.jpg"
        image_data = file.content

        try:
            cursor.execute("INSERT INTO images (image_name, image_data) VALUES (%s, %s)", (image_name, image_data))
            connection.commit()
            bot.send_message(received_message.chat.id, "✅ Image uploadée avec succès !")
        except Error as e:
            bot.send_message(received_message.chat.id, f"❌ Erreur lors de l'upload : {e}")
        finally:
            cursor.close()
            connection.close()

# Commande /search
@bot.message_handler(commands=['search'])
def list_images(message):
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
                image_id, date_uploaded = row
                bot.send_message(message.chat.id, f"ID: {image_id}\nDate: {date_uploaded}")

            bot.send_message(message.chat.id, "✏️ Envoyez l'ID de l'image à transférer au robot.")

            @bot.message_handler(func=lambda msg: msg.text.isdigit())
            def send_image_to_robot(msg):
                image_id = int(msg.text)
                cursor.execute("SELECT image_data FROM images WHERE id = %s", (image_id,))
                result = cursor.fetchone()

                if result:
                    image_data = result[0]
                    files = {'file': image_data}
                    try:
                        response = requests.post(f"{ESP32_URL}/upload", files=files)
                        if response.status_code == 200:
                            bot.send_message(msg.chat.id, "✅ Image transférée au robot.")
                        else:
                            bot.send_message(msg.chat.id, "❌ Échec du transfert.")
                    except Exception as e:
                        bot.send_message(msg.chat.id, f"❌ Erreur : {e}")
                else:
                    bot.send_message(msg.chat.id, f"⚠️ Aucune image trouvée avec l'ID {image_id}.")
    except Error as e:
        bot.send_message(message.chat.id, f"❌ Erreur lors de la recherche : {e}")
    finally:
        cursor.close()
        connection.close()

# Commandes pour les signaux
@bot.message_handler(commands=['pause'])
def pause_signal(message):
    try:
        requests.get(f"{ESP32_URL}/pause")
        bot.send_message(message.chat.id, "⏸️ Signal de pause envoyé au robot.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erreur : {e}")

@bot.message_handler(commands=['resume'])
def resume_signal(message):
    try:
        requests.get(f"{ESP32_URL}/resume")
        bot.send_message(message.chat.id, "▶️ Signal de reprise envoyé au robot.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erreur : {e}")

@bot.message_handler(commands=['cancel'])
def cancel_signal(message):
    try:
        requests.get(f"{ESP32_URL}/cancel")
        bot.send_message(message.chat.id, "❌ Signal d'annulation envoyé au robot.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erreur : {e}")

# Démarrer le bot
bot.polling()
