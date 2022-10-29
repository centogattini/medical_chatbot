import telebot
import consts

telebot.apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot('5514115973:AAEUGJilFHRu1NE8dqLh1p3RpXSKbCWAtPQ')

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.from_user.id,""" Здравствуйте. Это медицинский бот для 
    записи к врачу. ВЫ знаете к кому обратиться?""")
	keyboard = telebot.types.ReplyKeyboardMarkup(True,False)
	keyboard.add('Да')
	keyboard.add('Нет')
	
bot.infinity_polling(none_stop=True, interval=1)