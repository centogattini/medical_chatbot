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
    return f'{d} {dct[m]}'

#Проверка номера на корректность 
def check_number(number):
    check_number = re.search(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', test4)
    if bool(check_number) == True:
        return True  
    else: 
        return False
