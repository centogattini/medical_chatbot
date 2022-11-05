import telebot
from telebot import types

class TelegramBot:
	def __init__(self, token, clf, db, N=12):
		telebot.apihelper.ENABLE_MIDDLEWARE = True
		self.bot = telebot.TeleBot(token)
		self.classifier = clf
		self.database = db
		self.N = N

	def dialog(self):
		@self.bot.message_handler(commands=['start'])
		def start_message(message):

			keyboard = types.ReplyKeyboardMarkup(row_width=2)	
			btn1 = types.KeyboardButton(text = 'Да')
			btn2 = types.KeyboardButton(text = 'Нет')
			keyboard.add(btn1,btn2)
			self.bot.send_message(message.from_user.id,""" Здравствуйте. Это медицинский бот для 
			записи к врачу. Вы знаете к кому обратиться?""",reply_markup=keyboard)

		@self.bot.message_handler(commands=['text'])
		def first_question(message):
			if message.text == 'Да':	
				self.bot.send_message(message.from_user.id, "Напишите нам имя или профессию врача")
				self.bot.register_next_step_handler(message, name_or_prof)

			elif message.text == 'Нет':
				self.bot.send_message(message.from_user.id, "Пожалуйста, напишите нам свои симптомы")
				self.bot.register_next_step_handler(message, symp_recognition)

		@self.bot.message_handler(commands=['text'])
		def name_or_prof(message):
			self.bot.send_message(message.from_user.id,'1')

		@self.bot.message_handler(commands=['text'])
		def symp_recognition(message):
			self.bot.send_message(message.from_user.id,'2')


		self.bot.infinity_polling(none_stop=True, interval=1)
		##class with write and read