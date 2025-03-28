import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Список ID чатов или групп, куда будут пересылаться сообщения
TARGET_CHATS = [
    -1001234567890,  # Пример ID группы или канала
    -1009876543210,  # Замените на свои ID
]

def start(update, context):
    update.message.reply_text("Привет! Я бот для пересылки сообщений. Просто напиши сообщение, и я его отправлю в указанные чаты.")

def forward_message(update, context):
    message = update.message
    if message and message.text:
        for chat_id in TARGET_CHATS:
            try:
                context.bot.send_message(chat_id=chat_id, text=message.text)
            except Exception as e:
                logging.error(f"Ошибка при отправке в чат {chat_id}: {e}")

def main():
    # Токен должен быть задан в переменной окружения BOT_TOKEN
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("Не указан токен бота. Установите переменную окружения BOT_TOKEN")
    
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # Обработчик команды /start
    dp.add_handler(CommandHandler("start", start))
    # Обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
