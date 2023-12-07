import telebot
from telebot import types
import threading  # Импорт модуля threading
from datetime import datetime, timedelta

token = '6923109786:AAFmV2H5YUbGGbRO7DHn63eE3zp-KH0De78'
bot = telebot.TeleBot(token)

users_photos = {}  # Словарь для хранения фотографий от пользователей
reactions_count = {'❤️': 0, '❤️‍🔥': 0}  # Счетчик реакций к фотографиям
chat_id = '-1002004177366'  # Укажите ID чата, куда отправлять результаты

@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    user_id = message.from_user.id
    file_id = message.photo[-1].file_id
    users_photos[user_id] = file_id

    if len(users_photos) == 2:
        photo_1 = users_photos[list(users_photos.keys())[0]]
        photo_2 = users_photos[list(users_photos.keys())[1]]

        keyboard_1 = types.InlineKeyboardMarkup()
        keyboard_1.row(types.InlineKeyboardButton("❤️", callback_data='like_1'),
                        types.InlineKeyboardButton("❤️‍🔥", callback_data='fire_1'))

        bot.send_media_group(chat_id, [
            telebot.types.InputMediaPhoto(photo_1),
            telebot.types.InputMediaPhoto(photo_2)
        ], reply_markup=keyboard_1)

        # Запускаем таймер на 15 минут для подведения итогов голосования
        timer = threading.Timer(900, end_voting)
        timer.start()

def end_voting():
    winner = max(reactions_count, key=reactions_count.get)
    if winner == '❤️':
        winner_message = "В первом раунде победила фотография номер 1"
        bot.send_message(chat_id, winner_message)
        bot.send_photo(chat_id, users_photos[list(users_photos.keys())[0]])
    else:
        winner_message = "В первом раунде победила фотография номер 2"
        bot.send_message(chat_id, winner_message)
        bot.send_photo(chat_id, users_photos[list(users_photos.keys())[1]])

    # Очистка данных после отправки результатов
    users_photos.clear()
    reactions_count['❤️'] = 0
    reactions_count['❤️‍🔥'] = 0

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id

    if call.data == 'like_1':
        reactions_count['❤️'] += 1
    elif call.data == 'fire_1':
        reactions_count['❤️‍🔥'] += 1

    if reactions_count['❤️'] > reactions_count['❤️‍🔥']:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton("❤️", callback_data='like_1'),
                     types.InlineKeyboardButton("❤️‍🔥", callback_data='fire_1'))
        bot.send_photo(chat_id, users_photos[list(users_photos.keys())[0]], reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton("❤️", callback_data='like_2'),
                     types.InlineKeyboardButton("❤️‍🔥", callback_data='fire_2'))
        bot.send_photo(chat_id, users_photos[list(users_photos.keys())[1]], reply_markup=keyboard)

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
