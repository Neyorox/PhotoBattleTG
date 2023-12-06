from telegram.ext import Updater, CommandHandler, MessageHandler

# Замените YOUR_BOT_TOKEN на токен вашего бота
TOKEN = '5954372321:AAHttqBx7383OtFM-SO8_amUpul54SjiZFI'

# Функция-обработчик для получения фотографий от пользователей
def handle_photos(update, context):
    # Получаем объект пользователя и его идентификатор
    user = update.message.from_user
    user_id = user.id

    # Получаем список фотографий для текущего пользователя
    user_photos = context.user_data.setdefault(user_id, [])

    # Проверяем количество фотографий пользователя
    if len(user_photos) < 2:
        # Если фотографий меньше двух, добавляем текущую фотографию в список
        user_photos.append(update.message.photo[-1].file_id)
    else:
        # Если фотографий достаточно, пересылаем их в канал и очищаем список
        channel_id = '@your_channel_id'
        channel_text = 'Фотографии от пользователя {}:'.format(user_id)

        # Добавляем описание для каждой фотографии
        for photo_id in user_photos:
            channel_text += '\n{}'.format(photo_id)

        # Создаем объект бота и отправляем фотографии в канал
        bot = context.bot
        bot.send_message(chat_id=channel_id, text=channel_text)

        # Очищаем список фотографий пользователя
        user_photos.clear()

# Функция-обработчик для остальных сообщений пользователей
def handle_other(update, context):
    update.message.reply_text('Отправлять можно только фотографии')


def main():
    # Создаем объект-обновление


    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для обработки команд
    dispatcher = updater.dispatcher

    # Добавляем обработчики сообщений


    # Запускаем бота
    updater.start_polling()

if __name__ == '__main__':
    main()
