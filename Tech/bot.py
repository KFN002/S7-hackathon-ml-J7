import telebot
from telebot import types
from credentials import bot_token
from database import Database
from Tech.models.wing_inspection import WingInspectionModel
from Tech.models.engine_inspection import EngineInspectionModel
from file_handler import handle_uploaded_file
from question_handler import ask_question, handle_text
import os
from PIL import Image

wing_model = WingInspectionModel()
engine_model = EngineInspectionModel()
wing_model.eval()
engine_model.eval()

TOKEN = bot_token
bot = telebot.TeleBot(TOKEN)

db = Database("documents.db")

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🛩️ Инспекция крыла"))
    keyboard.add(types.KeyboardButton("⚙️ Инспекция агрегатов"))
    keyboard.add(types.KeyboardButton("📂 Загрузка документов"))
    keyboard.add(types.KeyboardButton("🔎 Задать вопрос"))
    return keyboard

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Выберите действие:", reply_markup=main_menu())


@bot.message_handler(content_types=['document'])
def handle_document(message):
    handle_uploaded_file(message, bot, db)


@bot.message_handler(func=lambda message: message.text == "📂 Загрузка документов")
def request_photo(message):
    bot.send_message(message.chat.id, "Отправьте документ (pdf) для анализа.")

@bot.message_handler(func=lambda message: message.text == "🛩️ Инспекция крыла" or message.text == "⚙️ Инспекция агрегатов")
def request_photo(message):
    analysis_type = "wing" if message.text == "🛩️ Инспекция крыла" else "engine"
    bot.send_message(message.chat.id, "Отправьте фото для анализа.")
    bot.register_next_step_handler(message, handle_photo, analysis_type)

@bot.message_handler(content_types=['photo'])
def handle_photo(message, analysis_type="wing"):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    file_path = f"{temp_dir}/{file_id}.jpg"
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    img = Image.open(file_path).convert('RGB')

    if analysis_type == "wing":
        result, level = wing_model.predict(img)
        bot.send_message(message.chat.id, f"🛩️ Инспекция крыла: {result} (Уровень: {level})")
    else:
        result, level = engine_model.predict(img)
        bot.send_message(message.chat.id, f"⚙️ Инспекция агрегатов: {result} (Уровень: {level})")

@bot.message_handler(func=lambda message: message.text == "🔎 Задать вопрос")
def ask_question_handler(message):
    ask_question(message, bot, db)

@bot.message_handler(func=lambda message: True)
def handle_text_handler(message):
    handle_text(message, bot, db)

if __name__ == "__main__":
    bot.polling(none_stop=True)
