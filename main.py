import telebot

token = '6923109786:AAFmV2H5YUbGGbRO7DHn63eE3zp-KH0De78'
bot = telebot.TeleBot(token)

users_photos = {}  # Словарь для хранения одной фотографии от каждого пользователя


# Обработчик получения фотографий и их совмещения
@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    user_id = message.from_user.id

    # Если у пользователя еще нет фотографии, сохраняем ее
    if user_id not in users_photos:
        file_id = message.photo[-1].file_id

        # Сохраняем file_id фотографии для данного пользователя
        users_photos[user_id] = file_id

        # Если у нас есть фотографии от двух пользователей, отправляем их вместе
        if len(users_photos) == 2:
            chat_id = '-1001996206227'
            if chat_id:
                try:
                    # Получаем информацию о пользователях
                    user1_info = message.from_user
                    user2_id = next(iter(users_photos.keys() - {user_id}))
                    user2_info = bot.get_chat_member(chat_id, user2_id)

                    # Получаем file_id фотографий от обоих пользователей
                    file_id_1 = users_photos[user_id]
                    file_id_2 = users_photos[user2_id]

                    # Отправляем обе фотографии вместе без описания
                    bot.send_media_group(chat_id, [
                        telebot.types.InputMediaPhoto(file_id_1),
                        telebot.types.InputMediaPhoto(file_id_2)
                    ])

                    # Формируем описание для сообщения с указанием отправителей
                    description = (
                        f"Фотографии от пользователя {user1_info} (@{user1_info}) и "
                        f"{user2_info.user.first_name} (@{user2_info.user.username})"
                    )

                    # Отправляем текстовое сообщение с описанием
                    bot.send_message(chat_id, description)

                    # Очищаем словарь фотографий после отправки
                    users_photos.clear()
                except Exception as e:
                    print(f"Ошибка при отправке фотографий: {e}")


# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    # Здесь можно добавить обработку текстовых сообщений, если необходимо
    pass


# Запуск бота
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Ошибка бота: {e}")
