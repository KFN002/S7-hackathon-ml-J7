import telebot
from telebot import types
from credentials import bot_token
from database import Database
from Tech.models.wing_inspection import WingInspectionModel
from Tech.models.engine_inspection import EngineInspectionModel
from file_handler import handle_uploaded_file
from question_handler import ask_question, handle_selected_document, handle_text

wing_model = WingInspectionModel()
engine_model = EngineInspectionModel()
wing_model.eval()
engine_model.eval()

TOKEN = bot_token
bot = telebot.TeleBot(TOKEN)

db = Database("documents.db")

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("📋 Совет по чек-листам"))
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

@bot.message_handler(func=lambda message: message.text == "🔎 Задать вопрос")
def ask_question_handler(message):
    ask_question(message, bot, db)

@bot.message_handler(func=lambda message: message.text in db.get_all_file_names())
def handle_selected_document_handler(message):
    handle_selected_document(message, bot, db)

@bot.message_handler(func=lambda message: True)
def handle_text_handler(message):
    handle_text(message, bot, db)

if __name__ == "__main__":
    bot.polling(none_stop=True)
