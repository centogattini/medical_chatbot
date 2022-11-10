import json
PATH_USER_DATA = 'data/user_data.json'

def add_user(user_id, globals):
    with open(PATH_USER_DATA,'r', encoding='utf-8') as f:
        data = json.load(f)
    data[user_id] = dict()
    for key, val in globals.items():
        data[user_id][key] = val
    with open(PATH_USER_DATA,'w', encoding='utf-8') as f:
        json.dump(data, f)
        
def set_user_data(user_id, key, val):
    with open(PATH_USER_DATA,'r', encoding='utf-8') as f:
        data = json.load(f)
    user_id = str(user_id)
    data[user_id][key] = val
    with open(PATH_USER_DATA,'w', encoding='utf-8') as f:
        json.dump(data, f)

def get_user_data(user_id, key):
    with open(PATH_USER_DATA,'r', encoding='utf-8') as f:
        data = json.load(f)
        user_id = str(user_id)
        if key in data[user_id]:
            return data[user_id][key]
        return None

import telebot
from telebot import types
from classifier import Classifier
from consts import CONST
from doctors_database import Database

telebot.apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot('5605255240:AAFO50CWDEDrQSoWUTU_Etw4tG5kwuu7VuI')
N_days = 10
N_times = 6
db = Database('data/database.db')
globals_dict = {'page_date':0,'page_time':0,'np_date':0,'np_time':0,
                'ans':'', 'tag':'error','picked_date':'',
                'picked_prof':'',
                'picked_time':'','picked_doc':''}
clf = Classifier(db.get_all_names(), db.get_symps_dict())##тут поменять
# функция для выведения расписания
def print_dates(bot, message, db):
    tag = get_user_data(message.from_user.id, 'tag')
    ans = get_user_data(message.from_user.id, 'ans')
    np_date = get_user_data(message.from_user.id,'np_date')
    if tag == 'name':

            dates = db.get_date_by_name(ans)

    if tag == 'prof':

            dates = db.get_date_by_profession(ans)
    page_date = get_user_data(message.from_user.id,'page_date')
    page_date += np_date
    set_user_data(message.from_user.id,'page_date',page_date)
    keyboard = types.ReplyKeyboardMarkup()

    curr_date = page_date*N_days
    while curr_date <= curr_date + N_days and curr_date < len(dates):
        keyboard.add(types.KeyboardButton(text=str(dates[curr_date])))
    btn1 = None
    btn2 = None
    if page_date == 0:
        btn1 = types.KeyboardButton(text=f'следующие {N_days} дат')
    if page_date*N_days + N_days >= len(dates):
        btn2 = types.KeyboardButton(text=f'предыдущие{N_days} дат')
    btn3 = types.KeyboardButton(text='выход')

    if btn1 and btn2:
        keyboard.row = (btn1, btn2)

    elif not btn1:
        keyboard.row(btn1)
        
    elif not btn2:
        keyboard.row(btn2)

    keyboard.row = (btn3)
    
    bot.edit_message_text( message.from_user.id,'Выберите дату для записи',
                         chat_id=message.chat.id, reply_markup=keyboard)
    bot.register_next_step_handler(message, ask_dates)

def print_times(bot, message, db):
    np_time = get_user_data(message.from_user.id, 'np_time')
    tag = get_user_data(message.from_user.id, 'tag')
    ans = get_user_data(message.from_user.id, 'ans')
    page_time = get_user_data(message.from_user.id,'page_time')
    page_time += np_time
    set_user_data(message.from_user.id,'page_time',page_time)
    if tag == 'prof':
        times = db.get_time_by_profession(message.text, ans.capitalize())
    elif tag == 'name':
        times = db.get_available_time(ans, message.text)
    keyboard = types.ReplyKeyboardMarkup()
    curr_time = page_time*N_times

    while curr_time<= curr_time + N_times and curr_time < len(times):
        keyboard.add(types.KeyboardButton(text=str(times[curr_time])))
        
    btn1 = None
    btn2 = None
    if page_time == 0:
        btn1 = types.KeyboardButton(text=f'следующие {N_times} талонов')
    if page_time*N_days + N_days >= len(times):
        btn2 = types.KeyboardButton(text=f'предыдущие{N_times} талонов')
    btn3 = types.KeyboardButton(text='возврат к выбору даты')

    if btn1 and btn2:
        keyboard.row = (btn1, btn2)

    elif not btn1:
        keyboard.row(btn1)
        
    elif not btn2:
        keyboard.row(btn2)

    keyboard.row = (btn3)
    bot.edit_message_text( message.from_user.id,'Выберите время для записи',
                         chat_id=message.chat.id, reply_markup=keyboard)
    bot.register_next_step_handler(message, ask_times)
#стартовое сообщение
@bot.message_handler(commands=['start'])
def start_message(message):
    globals_dict = {'page_date':0,'page_time':0,'np_date':0,'np_time':0,
                'ans':'', 'tag':'error','picked_date':'',
                'picked_prof':'',
                'picked_time':'','picked_doc':''}
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton(text='Да')
    btn2 = types.KeyboardButton(text='Нет')
    keyboard.add(btn1, btn2)
    bot.send_message(message.from_user.id, """ Здравствуйте. Это медицинский бот для \
    записи к врачу. Вы знаете к кому обратиться?""", reply_markup=keyboard)
    add_user(message.from_user.id, globals_dict)
    bot.register_next_step_handler(message, ask_1)

#обработка ответа на первое сообщение
@bot.message_handler(commands=['text'])
def ask_1(message):
    if message.text == 'Да':
        print('yes_1')
        bot.send_message(message.from_user.id,
                         "Напишите нам имя или профессию врача")
        bot.register_next_step_handler(message, ask_2)

    elif message.text == 'Нет':
        bot.send_message(message.from_user.id,
                         "Пожалуйста, напишите нам свои симптомы")
        bot.register_next_step_handler(message, symp_recognition)

#если человек знает к кому обратиться
@bot.message_handler(commands=['text'])
def ask_2(message):
    ##обрабатываем входную строку
    ans, tag = clf.identify_name_or_profession(message.text)
    set_user_data(message.from_user.id,'tag', tag)
    set_user_data(message.from_user.id,'ans', ans)
    #прописать соотвествующие тэги
    #если не смогли обработать имя или профессию
    if tag == 'error':

        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        btn1 = types.KeyboardButton(text='Да')
        btn2 = types.KeyboardButton(text='Нет')
        keyboard.add(btn1, btn2)

        bot.send_message(message.from_user.id, '''Кажется мы не нашли врача,
		который вам нужен. Мы можем записать вас к терапевту''', reply_markup=keyboard)
        bot.register_next_step_handler(message, answer_prof_name_error)

    else:
        print_dates(bot, message,db)


@bot.message_handler(commands=['text'])
def answer_prof_name_error(message):
    pass
@bot.message_handler(commands=['text'])
def symp_recognition(message):
    # bot.send_message(message.from_user.id, '')
    text = message.text
    ans, tag = clf.classify_symptoms(text)
    set_user_data(message.from_user.id,'ans',ans)
    set_user_data(message.from_user.id,'tag',tag)
    if tag == 'error':
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        btn_yes = types.KeyboardButton(text="Записаться к терапевту")
        btn_no = types.KeyboardButton(text="Нет")
        keyboard.add(btn_yes, btn_no)
        bot.send_message(message.from_user.id, 
                            f"Мы не знаем, к какому врачу вам обратиться, но можем \
                            записать вас к терапевту для подробной конслуьтации.",
                            reply_markup=keyboard)
        set_user_data(message.from_user.id, 'ans', 'терапевт')
        bot.register_next_step_handler(message, ask_3)

        return 
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    btn_yes = types.KeyboardButton(text="Да")
    btn_no = types.KeyboardButton(text="Нет")
    keyboard.add(btn_yes, btn_no)
    bot.send_message(message.from_user.id, 
                        f"Вы хотите записаться к {ans.capitalize()}y?",reply_markup=keyboard) 
                        # Может возникнуть проблема с дательным падежом
    set_user_data(message.from_user.id, 'picked_prof', ans)
    bot.register_next_step_handler(message, ask_5)

@bot.message_handler(commands=['text'])
def ask_5(message):
    if message.text == "Нет":
        return
    else:
        print_dates(bot, message, db)
@bot.message_handler(commands=['text'])
def ask_3(message):
    if message.text == "Записаться к терапевту":
        ans = "терапевт"
        set_user_data(message.from_user.id, 'ans', ans)
        print_dates(bot, message, db)
    else:
        # выход из диалога
        bye_failed()
         
@bot.message_handler(commands=['text'])
def ask_dates(message):
    if message.text == f'следующие {N_days} дат':
        set_user_data(message.from_user.id, 'np_date', 1)
        print_dates(bot, message, db)

    elif message.text == f'предыдущие {N_days} дат':
        set_user_data(message.from_user.id, 'np_date', -1)
        print_dates(bot, message, db)
    
    elif message.text =='выход':
        bot.send_message('До свидания!')

    else:
        tag = get_user_data(message.from_user.id,'tag')
        ans = get_user_data(message.from_user.id,'ans')
        picked_date = message.text
    print_times(bot, message)
# сказать пока, если человек не смог записаться к врачу

def bye_failed():
    pass

@bot.message_handler(commands=['text'])
def ask_times(message):
    if message.text == f'следующие {N_times} талонов':
        set_user_data(message.from_user.id,'np_time',1)
        print_times(bot, message, ans, tag, N_days)

    elif message.text == f'предыдущие {N_times} талонов':
        set_user_data(message.from_user.id,'np_time',1)
        print_times(bot, message)
    elif message.text == 'возврат к выбору даты':
        print_dates(bot, message)
        picked_date = None
    else:
        picked_time = message.text
        tag = get_user_data(message.from_user.id,'tag')
        ans = get_user_data(message.from_user.id,'ans')
        if tag == 'prof':
            docs = db.get_all_docs_by_datetime(ans, picked_date, picked_time)
            if len(docs)>0:
                picked_doc = docs[0]
        elif tag == 'name':
            picked_doc = ans
    
    bot.send_message(message.from_user.id,text="Введите свое ФИО")
            

bot.infinity_polling(none_stop=True, interval=1)
# class with write and read