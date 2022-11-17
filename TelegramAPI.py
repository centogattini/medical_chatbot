import telebot
from telebot import types
from utils import format_date, format_appointment
import json

PATH_USER_DATA = 'data/user_data.json'

def add_user(user_id, globals):
	with open(PATH_USER_DATA,'r', encoding='utf-8') as f:
		data = json.load(f)
	data[user_id] = dict()
	for key, val in globals.items():
		data[user_id][key] = val
	with open(PATH_USER_DATA,'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False)
		
def set_user_data(user_id, key, val):
	with open(PATH_USER_DATA,'r', encoding='utf-8') as f:
		data = json.load(f)
	user_id = str(user_id)
	data[user_id][key] = val
	with open(PATH_USER_DATA,'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False)

def get_user_data(user_id, key):
	with open(PATH_USER_DATA,'r', encoding='utf-8') as f:
		data = json.load(f)
		user_id = str(user_id)
		if key in data[user_id]:
			return data[user_id][key]
		return None
class TelegramBot:
	def __init__(self, token, clf, db, N=12):
		telebot.apihelper.ENABLE_MIDDLEWARE = True
		self.bot = telebot.TeleBot(token)
		self.classifier = clf
		self.db = db
		
	def start(self,):
		N_days = 10
		N_times = 6
		db = self.db
		globals_dict = {'page_date':0,'page_time':0,'np_date':0,'np_time':0,
						'ans':'', 'tag':'error','picked_date':'',
						'picked_prof':'','user_name':'',
						'picked_time':'','picked_doc':''}
		clf = self.classifier
		# функция для выведения расписания
		def print_dates(message):
			bot = self.bot
			tag = get_user_data(message.from_user.id, 'tag')
			ans = get_user_data(message.from_user.id, 'ans')
			np_date = get_user_data(message.from_user.id,'np_date')
			if tag == 'name':
				dates = db.get_date_by_name(ans)
			else:
				dates = db.get_date_by_profession(ans.capitalize())
				
			page_date = get_user_data(message.from_user.id,'page_date')
			page_date += np_date
			set_user_data(message.from_user.id,'page_date',page_date)
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width = 2)

			start_date = page_date*N_days
			curr_date = start_date
			while curr_date < start_date + N_days and curr_date < len(dates):
				keyboard.add(types.KeyboardButton(text=str(dates[curr_date])))
				curr_date += 1
			btn1 = None
			btn2 = None
			if page_date*N_days + N_days < len(dates):
				btn1 = types.KeyboardButton(text=f'следующие {N_days} дат')
			if page_date != 0:
				btn2 = types.KeyboardButton(text=f'предыдущие {N_days} дат')
			btn3 = types.KeyboardButton(text='выход')

			if btn1 and btn2:
				keyboard.row(btn2, btn1)

			elif btn1:
				keyboard.add(btn1)
				
			elif btn2:
				keyboard.add(btn2)

			keyboard.row(btn3)
			# last_message = get_user_data(message.from_user.id, 'last_message')
			# if last_message:
			#     bot.edit_message_text( message_id = last_message,text = 'Выберите дату для записи',
			#                         chat_id=message.chat.id, reply_markup=keyboard)
			# else:
			#     last_message = bot.send_message(message.from_user.id,'Выберите дату для записи', reply_markup=keyboard)
			#     set_user_data(message.from_user.id, 'last_message',last_message.id)
			bot.send_message(message.from_user.id,'Выберите дату для записи', reply_markup=keyboard)
			bot.register_next_step_handler(message, ask_dates)

		def print_times(message):
			np_time = get_user_data(message.from_user.id, 'np_time')
			tag = get_user_data(message.from_user.id, 'tag')
			ans = get_user_data(message.from_user.id, 'ans')
			page_time = get_user_data(message.from_user.id,'page_time')
			page_time += np_time

			set_user_data(message.from_user.id,'page_time',page_time)
			if tag == 'prof':
				times = self.db.get_time_by_profession(message.text, ans.capitalize())
			elif tag == 'name':
				times = self.db.get_available_time(ans, message.text)
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
			start_time = page_time*N_times
			curr_time = start_time

			while curr_time < start_time + N_times and curr_time < len(times):
				keyboard.add(types.KeyboardButton(text=str(times[curr_time])),)
				curr_time += 1
				
			btn1 = None
			btn2 = None
			if page_time*N_days + N_days >= len(times):
				btn1 = types.KeyboardButton(text=f'следующие {N_times} талонов')
			if page_time != 0:
				btn2 = types.KeyboardButton(text=f'предыдущие {N_times} талонов')
			btn3 = types.KeyboardButton(text='возврат к выбору даты')

			if btn1 and btn2:
				keyboard.row(btn1, btn2)
			elif btn1:
				keyboard.add(btn1)
			elif btn2:
				keyboard.add(btn2)

			keyboard.row(btn3)
			self.bot.send_message(message.from_user.id,'Выберите время для записи', reply_markup=keyboard)
			self.bot.register_next_step_handler(message, ask_times)

		#стартовое сообщение
		@self.bot.message_handler(commands=['start'])
		def start_message(message):
			globals_dict = {'page_date':0,'page_time':0,'np_date':0,'np_time':0,
						'ans':'', 'tag':'error','picked_date':'',
						'picked_prof':'','user_name':'',
						'picked_time':'','picked_doc':''}
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard= True)
			btn1 = types.KeyboardButton(text='Да')
			btn2 = types.KeyboardButton(text='Нет')
			btn3 = types.KeyboardButton(text='Посмотреть доступных врачей')
			btn4 = types.KeyboardButton(text='Мои талоны')
			keyboard.row(btn1, btn2)
			keyboard.add(btn3)
			keyboard.add(btn4)
			self.bot.send_message(message.from_user.id, "Здравствуйте. Это медицинский бот для записи к врачу." +
			 "\n\nВы знаете к кому обратиться?", reply_markup=keyboard)
			add_user(message.from_user.id, globals_dict)
			self.bot.register_next_step_handler(message, ask_1)

		def show_appointments(message):
			appointments = db.get_tickets(message.from_user.id)
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
			apppointments_str = ''
			for i in range(len(appointments)):
				apppointments_str += format_appointment(
					id=appointments[-1],
					patient=appointments[1],
					doctor=appointments[6], 
					profession=appointments[5], 
					date=appointments[3], 
					time=appointments[4]
					) + '\n'

			btn1 = types.KeyboardButton(text="Удалить запись к врачу")
			btn2 = types.KeyboardButton(text="Выход")
			keyboard.row(btn1, btn2)
			self.bot.send_message(message.from_user.id, appointments_str, reply_markup=keyboard, parse_mode="Markdown")
			self.bot.register_next_step_handler(message, ask_to_delete)	
		@self.bot.message_handler(commands=['text'])
		def ask_to_delete(message):
			if message.text == 'Удалить запись к врачу':
				appointments = db.get_tickets(message.from_user.id)
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
				for i in range(len(appointments)):
					btn = types.KeyboardButton(text=str(appointments[-1]))
					keyboard.add(btn)
				btn2 = types.KeyboardButton(text="Выход")
				keyboard.add(btn2)
				self.bot.send_message(message.from_user.id, "Выберете талон", reply_markup=keyboard, parse_mode="Markdown")
				self.bot.register_next_step_handler(message, ask_to_delete)	
				
			elif message.text == 'Выход':
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
				btn = types.KeyboardButton(text="\start")
				keyboard.add(btn)
				self.bot.send_message(message.from_user.id, "Чтобы записаться к врачу или посмотреть свои талоны нажмите кнопку /start", 
					reply_markup=keyboard)
				self.bot.register_next_step_handler(message, start_message)	
				
			else:	
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
				btn1 = types.KeyboardButton(text='Удалить запись к врачу')
				btn2 = types.KeyboardButton(text='Выход')
				keyboard.add(btn1, btn2)
				self.bot.send_message(message.from_user.id, 
				f"Мы не распознали ваш ответ. Пожалуйста, воспользуйтесь кнопками",reply_markup=keyboard)
				self.bot.register_next_step_handler(message, ask_to_delete)	
					
		#обработка ответа на первое сообщение
		@self.bot.message_handler(commands=['text'])
		def ask_1(message):
			if message.text == 'Нет':
				self.bot.send_message(message.from_user.id,
								"Пожалуйста, напишите нам свои симптомы")
				self.bot.register_next_step_handler(message, symp_recognition)
			
			elif message.text == 'Да':
				self.bot.send_message(message.from_user.id,
								"Напишите нам имя или профессию врача")
				self.bot.register_next_step_handler(message, ask_2)

			elif message.text == "Посмотреть доступных врачей":
				alldocs = self.db.get_all_doc_n_names()
				alldocs_str = ''
				for prof, name in alldocs:
					alldocs_str += prof + ", " + name + "\n"
				self.bot.send_message(message.from_user.id,
								alldocs_str)
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard= True)

				btn1 = types.KeyboardButton(text='Да')
				btn2 = types.KeyboardButton(text='Нет')
				keyboard.row(btn1, btn2)			
				self.bot.send_message(message.from_user.id, "Вы знаете к кому обратиться?", reply_markup=keyboard)
				self.bot.register_next_step_handler(message, ask_1)
			elif message.text == "Мои талоны":
				show_appointments(message)
			else:
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard= True)
				btn1 = types.KeyboardButton(text='Да')
				btn2 = types.KeyboardButton(text='Нет')
				keyboard.add(btn1, btn2)
				self.bot.send_message(message.from_user.id, 
				f"Мы не распознали ваш ответ. Пожалуйста, воспользуйтесь кнопками",reply_markup=keyboard)
				self.bot.register_next_step_handler(message, ask_1)

		#если человек знает к кому обратиться
		@self.bot.message_handler(commands=['text'])
		def ask_2(message):
			if not type(message.text) is str:
				self.bot.send_message(message.from_user.id, 
				f"Мы не распознали ваш ответ. Пожалуйста, напишите имя или профессию врача",reply_markup=keyboard)
				self.bot.register_next_step_handler(message, ask_2)
			##обрабатываем входную строку
			ans, tag = clf.identify_name_or_profession(message.text)
			set_user_data(message.from_user.id,'tag', tag)
			set_user_data(message.from_user.id,'ans', ans)
			#прописать соотвествующие тэги
			#если не смогли обработать имя или профессию
			if tag == 'error':

				keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True, one_time_keyboard= True)
				btn1 = types.KeyboardButton(text="Записаться к терапевту")
				btn2 = types.KeyboardButton(text='Нет')
				keyboard.add(btn1, btn2)

				self.bot.send_message(message.from_user.id,
					'Кажется мы не нашли врача,который вам нужен. Мы можем записать вас к терапевту', 
					reply_markup=keyboard)
				self.bot.register_next_step_handler(message, ask_3)
			elif tag == 'autocorr':
				
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True, one_time_keyboard= True)
				btn1 = types.KeyboardButton(text="Да")
				btn2 = types.KeyboardButton(text="Нет")
				keyboard.add(btn1, btn2)

				self.bot.send_message(message.from_user.id,
					f'Возможно, вы имели ввижу "{ans}"?', 
					reply_markup=keyboard)
				self.bot.register_next_step_handler(message, message_correct)
				
			else:
				print_dates(message)


		@self.bot.message_handler(commands=['text'])
		def symp_recognition(message):
			text = message.text
			ans, tag = clf.classify_symptoms(text)
			set_user_data(message.from_user.id,'ans',ans)
			set_user_data(message.from_user.id,'tag',tag)
			if tag == 'error':
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True, one_time_keyboard= True)
				btn_yes = types.KeyboardButton(text="Записаться к терапевту")
				btn_no = types.KeyboardButton(text="Нет")
				keyboard.add(btn_yes, btn_no)
				self.bot.send_message(message.from_user.id, 
									f"Мы не знаем, к какому врачу вам обратиться, но можем записать вас к терапевту для подробной консультации.",
									reply_markup=keyboard)
				set_user_data(message.from_user.id, 'ans', 'терапевт')
				self.bot.register_next_step_handler(message, ask_3)

				return 
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True, one_time_keyboard= True)
			btn_yes = types.KeyboardButton(text="Да")
			btn_no = types.KeyboardButton(text="Нет")
			keyboard.add(btn_yes, btn_no)
			self.bot.send_message(message.from_user.id, 
								f"Вы хотите записаться к {ans}y?",reply_markup=keyboard) 
								# Может возникнуть проблема с дательным падежом
			set_user_data(message.from_user.id, 'picked_prof', ans)
			self.bot.register_next_step_handler(message, ask_5)

		@self.bot.message_handler(commands=['text'])
		def ask_5(message):
			if message.text == "Нет":
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
				btn1 = types.KeyboardButton('/start')
				keyboard.add(btn1)
				self.bot.send_message(message.from_user.id, 'До свидания!', reply_markup=keyboard)
			elif message.text == "Да":
				print_dates(message)
			else:
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard= True)
				btn1 = types.KeyboardButton(text='Да')
				btn2 = types.KeyboardButton(text='Нет')
				keyboard.add(btn1, btn2)
				self.bot.send_message(message.from_user.id, 
				f"Мы не распознали ваш ответ. Пожалуйста, воспользуйтесь кнопками",reply_markup=keyboard)
				self.bot.register_next_step_handler(message, ask_5)

		@self.bot.message_handler(commands=['text'])
		def message_correct(message):
			if message.text == "Нет":
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard= True)
				btn1 = types.KeyboardButton(text='Да')
				btn2 = types.KeyboardButton(text='Выход')
				keyboard.add(btn1, btn2)
				self.bot.send_message(message.from_user.id, 
					f"Хотите выбрать врача из списка?",reply_markup=keyboard)
				self.bot.register_next_step_handler(message, choose_doctors_from_list)
			elif message.text == "Да":
				print_dates(message)
			else:
				self.botbot.send_message(message.from_user.id, 
					f"Мы не распознали ваш ответ. Пожалуйста, воспользуйтесь кнопками",reply=keyboard)
				self.bot.register_next_step_handler(message, message_correct)

		@self.bot.message_handler(commands=['text'])
		def choose_doctors_from_list(message):
			if message.text == 'Да':
				print_docs(message)
			elif message.text == 'Выход':
				bye_failed(message)
		
		def bye_failed(message):
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
			btn = types.KeyboardButton(text='\start')
			keyboard.add(btn1)
			self.bot.send_message(message.from_user.id, 
				f"К сожалению, мы не смогли записать Вас к врачу. \nЧтобы попробовать еще раз нажмите кнопку /start'",reply=keyboard)
			self.bot.register_next_step_handler(message, start_message) 

		@self.bot.message_handler(commands=['text'])
		def ask_3(message):
			if message.text == "Записаться к терапевту":
				ans = "терапевт"
				set_user_data(message.from_user.id,'tag','prof')
				set_user_data(message.from_user.id, 'ans', ans)
				print_dates(message)
			elif message.text == "Нет":
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
				btn1 = types.KeyboardButton(f'/start')
				keyboard.add(btn1)
				self.bot.send_message(message.from_user.id,'До свидания!', reply_markup=keyboard)
			else:
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard= True)
				btn1 = types.KeyboardButton(text='Записаться к терапевту')
				btn2 = types.KeyboardButton(text='Нет')
				keyboard.add(btn1, btn2)
				self.bot.send_message(message.from_user.id, 
				f"Мы не распознали ваш ответ. Пожалуйста, воспользуйтесь кнопками",reply_markup=keyboard)
				self.bot.register_next_step_handler(message, ask_3)

		@self.bot.message_handler(commands=['text'])
		def ask_dates(message):
			if message.text == f'следующие {N_days} дат':
				set_user_data(message.from_user.id, 'np_date', 1)
				print_dates(message)

			elif message.text == f'предыдущие {N_days} дат':
				set_user_data(message.from_user.id, 'np_date', -1)
				print_dates(message)
			
			elif message.text =='выход':
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
				btn1 = types.KeyboardButton(f'/start')
				keyboard.add(btn1)
				self.bot.send_message(message.from_user.id,'До свидания!', reply_markup=keyboard)

			else:
				tag = get_user_data(message.from_user.id,'tag')
				ans = get_user_data(message.from_user.id,'ans')
				if tag == 'prof':
					dates = db.get_date_by_profession(ans.capitalize())
				elif tag == 'name':
					dates = db.get_date_by_name(ans)

				if not message.text in dates:
					self.bot.send_message(message.from_user.id,"Некорректная дата, выберите еще раз ")
					print_dates(message)
					return
				set_user_data(message.from_user.id,'picked_date', message.text)
				picked_date = message.text
				#set_user_data(message.from_user.id,'last_message',None)
				print_times(message)
		# сказать пока, если человек не смог записаться к врачу

		@self.bot.message_handler(commands=['text'])
		def ask_times(message):
			if message.text == f'следующие {N_times} талонов':
				set_user_data(message.from_user.id,'np_time',1)
				print_times(message)

			elif message.text == f'предыдущие {N_times} талонов':
				set_user_data(message.from_user.id,'np_time',1)
				print_times(message)
			elif message.text == 'возврат к выбору даты':
				print_dates(message)
				set_user_data(message.from_user.id,'picked_date', None)
			else:
				set_user_data(message.from_user.id,'picked_time', message.text)
				tag = get_user_data(message.from_user.id,'tag')
				ans = get_user_data(message.from_user.id,'ans')
				if tag == 'prof':
					docs = db.get_all_docs_by_datetime(ans.capitalize(), get_user_data(message.from_user.id,
					'picked_date'), get_user_data(message.from_user.id,'picked_time'))
					if len(docs)>0:
						set_user_data(message.from_user.id,'picked_doc', docs[0])
					else:
						set_user_data(message.from_user.id,'picked_doc', docs)
				elif tag == 'name':
					set_user_data(message.from_user.id,'picked_doc', ans)
			
				self.bot.send_message(message.from_user.id,text="Введите свое ФИО")
				self.bot.register_next_step_handler(message, ask_number)

		@self.bot.message_handler(commands=['text'])
		def ask_number(message):
			set_user_data(message.from_user.id, 'user_name', message.text)
			self.bot.send_message(message.from_user.id, text="Введите свой номер телефона")
			self.bot.register_next_step_handler(message, bye_successful)

		@self.bot.message_handler(commands=['text'])
		def bye_successful(message):
			db.record_inf(get_user_data(message.from_user.id, 'user_name'), message.text,
			get_user_data(message.from_user.id, 'picked_date'),get_user_data(message.from_user.id, 'picked_time'),
			get_user_data(message.from_user.id, 'picked_doc'))
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
			btn1 = types.KeyboardButton(f'/start')
			keyboard.add(btn1)
			self.bot.send_message(message.from_user.id,
			f'Спасибо за обращение!\n\nВы записаны к врачу\n{get_user_data(message.from_user.id,"picked_doc")}\nДень приема: {format_date(get_user_data(message.from_user.id,"picked_date"))}\nВремя приема: {(get_user_data(message.from_user.id,"picked_time"))}',reply_markup = keyboard)

		self.bot.infinity_polling(none_stop=True, interval=1)
		# class with write and read

