import telebot
from telebot import types
import threading
from datetime import datetime, timedelta

token = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(token)

users_photos = {}
reactions_count = {'❤️': 0, '❤️‍🔥': 0}
chat_id = 'YOUR_CHAT_ID'

@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    user_id = message.from_user.id
    file_id = message.photo[-1].file_id
    users_photos[user_id] = file_id

    if len(users_photos) == 2:
        photo_1 = users_photos[list(users_photos.keys())[0]]
        photo_2 = users_photos[list(users_photos.keys())[1]]

        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton("❤️", callback_data='like_1'),
                     types.InlineKeyboardButton("❤️‍🔥", callback_data='fire_1'),
                     types.InlineKeyboardButton("❤️", callback_data='like_2'),
                     types.InlineKeyboardButton("❤️‍🔥", callback_data='fire_2'))

        bot.send_media_group(chat_id, [
            telebot.types.InputMediaPhoto(photo_1),
            telebot.types.InputMediaPhoto(photo_2)
        ], reply_markup=keyboard)

        # Starting a timer for 15 minutes to end the voting
        timer = threading.Timer(900, end_voting)
        timer.start()

def end_voting():
    winner = max(reactions_count, key=reactions_count.get)
    if winner == '❤️':
        winner_message = "Фотография номер 1 победила!"
        bot.send_message(chat_id, winner_message)
        bot.send_photo(chat_id, users_photos[list(users_photos.keys())[0]])
    else:
        winner_message = "Фотография номер 2 победила!"
        bot.send_message(chat_id, winner_message)
        bot.send_photo(chat_id, users_photos[list(users_photos.keys())[1]])

    # Clearing data after sending the results
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
    elif call.data == 'like_2':
        reactions_count['❤️'] += 1
    elif call.data == 'fire_2':
        reactions_count['❤️‍🔥'] += 1

if __name__ == '__main__':
    bot.polling(none_stop=True)
