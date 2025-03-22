from telebot import types
from Tech.chat_assistant import get_advice_from_docs
from Tech.document_parser import processor


def ask_question(message, bot, db):
    files = db.get_all_file_names()
    if not files:
        bot.send_message(message.chat.id, "Нет загруженных документов. Сначала загрузите файл.")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for file in files:
        keyboard.add(types.KeyboardButton(file))
    bot.send_message(message.chat.id, "Выберите документ для анализа:", reply_markup=keyboard)


def handle_selected_document(message, bot, db):
    file_path = db.get_file_path(message.text)
    if not file_path:
        bot.send_message(message.chat.id, "Файл не найден.")
        return

    text = processor.process_file(file_path)
    processor.documents[message.text] = text
    bot.send_message(message.chat.id, "Теперь отправьте ваш вопрос.")


def handle_text(message, bot, db):
    if processor.documents:
        response = get_advice_from_docs(message.text)
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Нет загруженных документов для анализа.")
