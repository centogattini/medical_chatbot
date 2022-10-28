import calendar
from datetime import datetime
import sqlite3

# if __name__ == '__main__':

con = sqlite3.connect('timetable.db')
cur = con.cursor()

#Формируем столбцы временных окон
time_var = ''
for i in range(9, 19):
    time_var+=(f"t{i} BOOL, t{i}30 BOOL, ")

time_var+=("t19 BOOL, t1930 BOOL")

#Создаем таблицу
cur.execute('CREATE TABLE timetable(profession VARCHAR(255), name VARCHAR(255), date DATE, {})'.format(time_var))
con.commit()


#Заполняем данные о времени на день
def fill_time(start, stop):
    time = []
    #0 - свободно
    #1 - занято
    for i in range(9, 20):
        if i >= start and i < stop:
            time.append(0)
            time.append(0)
        else:
            time.append(1)
            time.append(1)

    return str(time)[1:-1]


#Заводим календарь расписания
my_calendar = calendar.Calendar(firstweekday=0)

#Текущая дата
curYear = datetime.now().year
curMonth = datetime.now().month
curDay = datetime.now().day

recording = [] 
delta_time = 3 

year = curYear
month = curMonth
for m in range(curMonth, curMonth+delta_time):
    #Заполняем данные на месяц 

    if month > 12:
        month%=12
        year+=1


    days = []
    for i in range(7):
        days.append([])

    
    for date in my_calendar.monthdayscalendar(year, month):
        for i in range(7):
            if date[i] != 0 and (date[i] >= curDay or month > curMonth or year > curYear):
                days[i].append(date[i])
        
    
    recording.append(days)


    #Разбиваем все дни месяца по дням недели
    Monday = recording[-1][0]
    Tuesday = recording[-1][1]
    Wednesday = recording[-1][2]
    Thursday = recording[-1][3]
    Friday = recording[-1][4]
    Saturday = recording[-1][5]
    Sunday = recording[-1][6]

    #Терапевт
    #____________________________________________________
    dates_ther = sorted(Monday + Wednesday + Friday)
    time_ther = fill_time(9, 16)

    for d in dates_ther:
        cur.execute('INSERT INTO timetable VALUES("Терапевт", "Айболит Сергей Сергеевич", "{0}-{1}-{2}", {3})'.format(year, month, str(d), time_ther))
    con.commit()


    #Хирург
    #____________________________________________________
    dates_surg = sorted(Tuesday + Saturday)
    time_surg = fill_time(10, 14)

    for d in dates_surg:
        cur.execute('INSERT INTO timetable VALUES("Хирург", "Резник Максим Владимирович", "{0}-{1}-{2}", {3})'.format(year, month, str(d), time_surg))
    con.commit()


    #Гастроэнтеролог
    #____________________________________________________
    dates_gastr = sorted(Tuesday + Friday)
    time_gastr = fill_time(14, 20)

    for d in dates_gastr:
        cur.execute('INSERT INTO timetable VALUES("Гастроэнтеролог", "Пузикова Лидия Васильевна", "{0}-{1}-{2}", {3})'.format(year, month, str(d), time_gastr))
    con.commit()

    #Кардиолог
    #____________________________________________________
    dates_card = sorted(Monday + Wednesday + Saturday)
    time_card = fill_time(15, 19) 

    for d in dates_card:
        cur.execute('INSERT INTO timetable VALUES("Кардиолог", "Ишемитов Марат Ренатович", "{0}-{1}-{2}", {3})'.format(year, month, str(d), time_card))
    con.commit()

    month+=1