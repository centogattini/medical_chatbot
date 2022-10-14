import sqlite3

if __name__ == '__main__':
    con = sqlite3.connect('timetable.db')
    cur = con.cursor()

    #Формируем столбцы временных окон
    time_var = ''
    for i in range(9, 19):
        time_var+=(f"t{i} BOOL, t{i}30 BOOL, ")

    time_var+=("t19 BOOL, t1930 BOOL")

    #Создаем таблицуs
    cur.execute('CREATE TABLE timetable(profession VARCHAR(255), name VARCHAR(255), date DATE, {})'.format(time_var))
    con.commit()

    #Терапевт
    #____________________________________________________
    dates_ther = [3, 5, 7]
    for i in range(1, 4):
        dates_ther.append(dates_ther[0]+7*i)
        dates_ther.append(dates_ther[1]+7*i)
        dates_ther.append(dates_ther[2]+7*i)


    #0 - свободно
    #1 - занято
    time_ther = []
    for i in range(9, 20):
        if i >= 9 and i < 16:
            time_ther.append(0)
            time_ther.append(0)        
        else:
            time_ther.append(1)
            time_ther.append(1)

    time_ther = str(time_ther)[1:-1]

    # print(dates_ther)
    # print(time_ther)

    for d in dates_ther:
        cur.execute('INSERT INTO timetable VALUES("Терапевт", "Айболит Сергей Сергеевич", "2022-10-{0}", {1})'.format(str(d), time_ther))

    con.commit()

    #Хирург
    #____________________________________________________
    dates_surg = [4, 8]
    for i in range(1, 4):
        dates_surg.append(dates_surg[0]+7*i)
        dates_surg.append(dates_surg[1]+7*i)

    #0 - свободно
    #1 - занято
    time_surg = []
    for i in range(9, 20):
        if i >= 10 and i < 14:
            time_surg.append(0)
            time_surg.append(0)        
        else:
            time_surg.append(1)
            time_surg.append(1)

    time_surg = str(time_surg)[1:-1]

    # print(dates_surg)
    # print(time_surg)

    for d in dates_surg:
        cur.execute('INSERT INTO timetable VALUES("Хирург", "Резник Максим Владимирович", "2022-10-{0}", {1})'.format(str(d), time_surg))

    con.commit()


    #Гастроэнтеролог
    #____________________________________________________
    dates_gastr = [4, 7]
    for i in range(1, 4):
        dates_gastr.append(dates_gastr[0]+7*i)
        dates_gastr.append(dates_gastr[1]+7*i)


    #0 - свободно
    #1 - занято
    time_gastr = []
    for i in range(9, 20):
        if i >= 14 and i < 20:
            time_gastr.append(0)
            time_gastr.append(0)        
        else:
            time_gastr.append(1)
            time_gastr.append(1)

    time_gastr = str(time_gastr)[1:-1]

    # print(dates_gastr)
    # print(time_gastr)

    for d in dates_gastr:
        cur.execute('INSERT INTO timetable VALUES("Гастроэнтеролог", "Пузикова Лидия Васильевна", "2022-10-{0}", {1})'.format(str(d), time_gastr))

    con.commit()

    #Кардиолог
    #____________________________________________________
    dates_card = [3, 5, 8]
    for i in range(1, 4):
        dates_card.append(dates_card[0]+7*i)
        dates_card.append(dates_card[1]+7*i)
        dates_card.append(dates_card[2]+7*i)


    #0 - свободно
    #1 - занято
    time_card = []
    for i in range(9, 20):
        if i >= 15 and i < 19:
            time_card.append(0)
            time_card.append(0)        
        else:
            time_card.append(1)
            time_card.append(1)

    time_card = str(time_card)[1:-1]