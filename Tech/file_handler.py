import os


def handle_uploaded_file(message, bot, db):
    file_id = message.document.file_id
    file_name = message.document.file_name
    file_path = f"files/{file_name}"

    if db.document_exists(file_id):
        bot.send_message(message.chat.id, "Этот документ уже был загружен.")
        return

    os.makedirs("files", exist_ok=True)
    downloaded_file = bot.get_file(file_id)

    with open(file_path, 'wb') as new_file:
        new_file.write(bot.download_file(downloaded_file.file_path))

    db.insert_document(file_id, file_name, file_path)
    bot.send_message(message.chat.id, "Документ загружен и сохранён.")