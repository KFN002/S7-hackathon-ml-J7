import os
import torch
import telebot
from telebot import types
from PIL import Image
from models.wing_inspection import WingInspectionModel
from models.engine_inspection import EngineInspectionModel
from chat_assistant import get_checklist_advice

# Загрузим модели
wing_model = WingInspectionModel()
engine_model = EngineInspectionModel()
wing_model.load_state_dict(torch.load("models/wing_model.pth", map_location=torch.device('cpu')))
engine_model.load_state_dict(torch.load("models/engine_model.pth", map_location=torch.device('cpu')))
wing_model.eval()
engine_model.eval()

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)


def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("📋 Check-list Advice"))
    keyboard.add(types.KeyboardButton("🛩️ Wing Inspection"))
    keyboard.add(types.KeyboardButton("⚙️ Engine Inspection"))
    return keyboard


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Выберите действие:", reply_markup=main_menu())


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = f"temp/{file_id}.jpg"
    os.makedirs("temp", exist_ok=True)

    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    img = Image.open(file_path).convert('RGB')

    bot.send_message(message.chat.id, "Выберите, что анализировать: крыло или агрегат", reply_markup=main_menu())


@bot.message_handler(func=lambda message: message.text == "🛩️ Wing Inspection")
def wing_inspection(message):
    bot.send_message(message.chat.id, "Отправьте фото крыла для анализа.")


@bot.message_handler(func=lambda message: message.text == "⚙️ Engine Inspection")
def engine_inspection(message):
    bot.send_message(message.chat.id, "Отправьте фото двигателя для анализа.")


@bot.message_handler(func=lambda message: message.text == "📋 Check-list Advice")
def checklist_advice(message):
    bot.send_message(message.chat.id, "Введите вопрос или проблему, и я помогу с советами по чек-листу.")


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    response = get_checklist_advice(message.text)
    bot.send_message(message.chat.id, response, reply_markup=main_menu())


if __name__ == "__main__":
    bot.polling(none_stop=True)
