import re
#Преобразуем кортеж (1, 0, ...) свободного времени в лист вида [9:00, 9:30, ..]
def time_to_text(time):
    res = []
    h = '9'
    m = '00'
    for i in time:
        cur_time = h + ":" + m
        if m == '00':
            m = '30'
        else:
            h = str(int(h)+1)
            m = '00'

        if i == 0:
            res.append(cur_time)

    return res

def format_date(date):
    m = date[5:7]
    d = date[-2:]
    dct = {
        '01':'января',
        '02':'февраля',
        '03':'марта',
        '04':'апреля',
        '05':'мая',
        '06':'июня',
        '07':'июля',
        '08':'августа',
        '09':'сентября',
        '10':'октября',
        '11':'ноября',
        '12':'декабря',
    }
    return f'{int(d)} {dct[m]}'

def format_time(time):
    # Input: time in format "HH:MM:SS"
    # Output: time in format "HH:MM"
    return time[:-3] 

def format_appointment(id, patient, doctor, profession, date, time):
    s = f'Талон <b>{id}</b>\nПациент: {patient}\n' + \
            f'Врач: {doctor}, {profession.capitalize()}\n' + \
            f'Дата и время приема {format_date(date)} {format_time(time)}' 
    return s

#Проверка номера на корректность 
def is_number(number):
    check_number = re.fullmatch(r'^(\+7|7|8)?[\s\-]?\(?[3489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', number)
    if bool(check_number) == True:
        return True  
    else: 
        return False

#Проверка имени на корректность
def is_name(name):
    name = name.replace(" ", "")
    print(name)
    incorrect_symbols = re.search(r'[^а-яА-ЯёЁ]', name)

    if bool(incorrect_symbols) == False:
        return True
    else:
        return False

def reformat_date(formated_date):
    # Input: Date in format %n имя_месяца (в родительном падеже)
    # Output: YYYY-MM-DD
    from datetime import date
    today = date.today()
    today_year = int(today.year)
    today_month = int(today.month)

    dct = {
        'января':'01',
        'февраля':'02',
        'марта':'03',
        'апреля':'04',
        'мая':'05',
        'июня':'06',
        'июля':'07',
        'августа':'08',
        'сентября':'09',
        'октября':'10',
        'ноября':'11',
        'декабря':'12'
    }

    fday, fmonth = formated_date.split()
    reformated_day = fday if int(fday) >= 10 else f"0{fday}"
    reformated_month = dct[fmonth]
    reformated_year = str(today_year) if (int(reformated_month) >= today_month) else str(today_year+1)
    return f'{reformated_year}-{reformated_month}-{reformated_day}'
    


    