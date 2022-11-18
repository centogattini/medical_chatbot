import sqlite3, datetime, utils

#Текущая дата
curYear = datetime.datetime.now().year
curMonth = datetime.datetime.now().month
curDay = datetime.datetime.now().day

class Database():

    def __init__(self, path):
        self.path = path
        con = sqlite3.connect(self.path)
        cur = con.cursor()
    
    #Получить время на выбранную дату по имени врача
    def get_available_time(self, name, date):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        res = cur.execute(f'SELECT\
            t9, t930, t10, t1030, t11, t1130, t12, t1230, t13, t1330, \
            t14, t1430, t15, t1530, t16, t1630, t17, t1730, t18, t1830, t19, t1930 \
            FROM timetable \
            AS T WHERE T.date = "{date}" AND T.name = "{name}"')
        
        if not res:
            return None

        fetch = res.fetchall()
        if not fetch:
            return None
        
        return utils.time_to_text(fetch[0])

    #Возращает все свободные даты по имени в формате YYYY-MM-DD
    def get_date_by_name(self, name):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        #добавить от сегодняшнего дня, а не от момента создания таблицы и order by
        res = cur.execute(f'SELECT date FROM timetable WHERE date >= DATE("now") AND name = "{name}" AND (t9 = 0 OR t930 = 0 OR t10 = 0 OR t1030 = 0 OR t11 = 0 OR t1130 = 0 OR t12 = 0 OR t1230 = 0 OR t13 = 0 OR t1330 = 0 OR t14 = 0 OR t1430 = 0 OR t15 = 0 OR t1530 = 0 OR t16 = 0 OR t1630 = 0 OR t17 = 0 OR t1730 = 0 OR t18 = 0 OR t1830 = 0 OR t19 OR t1930) ORDER BY date ASC')
        res = res.fetchall()
        dates = []
        for i in res:
            dates.append(i[0])

        return dates

    #Возращает все свободные даты по профессии в формате YYYY-MM-DD
    def get_date_by_profession(self, profession):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        res = cur.execute(f'SELECT DISTINCT date FROM timetable WHERE date >= DATE("now") AND profession = "{profession}" AND (t9 = 0 OR t930 = 0 OR t10 = 0 OR t1030 = 0 OR t11 = 0 OR t1130 = 0 OR t12 = 0 OR t1230 = 0 OR t13 = 0 OR t1330 = 0 OR t14 = 0 OR t1430 = 0 OR t15 = 0 OR t1530 = 0 OR t16 = 0 OR t1630 = 0 OR t17 = 0 OR t1730 = 0 OR t18 = 0 OR t1830 = 0 OR t19 OR t1930) ORDER BY date ASC')
        res = res.fetchall()
        dates = []
        for i in res:
            dates.append(i[0])

        return dates

    #Возвращает все свободные талоны на дату для всех врачей данной профессии
    def get_time_by_profession(self, date, profession):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        res = cur.execute(f'SELECT\
            t9, t930, t10, t1030, t11, t1130, t12, t1230, t13, t1330, \
            t14, t1430, t15, t1530, t16, t1630, t17, t1730, t18, t1830, t19, t1930 \
            FROM timetable \
            AS T WHERE T.date = "{date}" AND T.profession = "{profession}"')
        if not res:
            return None
        ans = []
        for t in(res.fetchall()):
            ans += utils.time_to_text(t)
        
        ans = list(set(ans))
        ans_3 = sorted([x for x in ans if len(x) == 4])
        ans_4 = sorted([x for x in ans if len(x) == 5])
        
        return ans_3 + ans_4

    #Возвращает всех доступных врачей данной профессии по дате и времени
    def get_all_docs_by_datetime(self, profession, date, time):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        #Преобразуем время вида 9:30 к названию столбца вида t930 
        if time[-2:] != '00':
            time = 't' + time[:-3] + time[-2:]
        else:
            time = 't' + time[:-3]

        res = cur.execute(f'SELECT name FROM timetable AS T \
            WHERE T.profession = "{profession}" AND T.date = "{date}" AND T.{time} = 0')


        return [doc[0] for doc in res.fetchall()]

    #Произвести запись в расписание 
    def set_appointment(self, time, name, date): 
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        #hh:mm:ss -> thhmm   
        time = Database.format_time(time)

        try:
            cur.execute(f'UPDATE timetable AS T SET "{time}" = 1 WHERE T.name = "{name}" AND T.date = "{date}"')
            con.commit()
            return 0
        except:
            raise Exception

    #Получить множество всех врачей с именами
    def get_all_doc_n_names(self)->list:
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        res = cur.execute(f'SELECT DISTINCT profession, name \
                            FROM timetable \
                            ORDER BY profession ASC')
        res = [r for r in res.fetchall()]
        return res
    
    #Получить множество имен всех врачей
    def get_all_names(self)->list:
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        res = cur.execute(f'SELECT DISTINCT name FROM timetable')
        res = set([r[0] for r in res.fetchall()])
        return list(res)

    #Получить множество всех профессии врачей 
    def get_all_professions(self)->list:
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        res = cur.execute(f'SELECT DISTINCT profession FROM timetable')
        res = set(r[0] for r in res.fetchall())
        return list(res)

    #Получить словарь вида {врач:симптомы}
    def get_symps_dict(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        professions = cur.execute('SELECT DISTINCT profession FROM symptoms') 
        lst_docs = []
        lst_symps = []

        for doc in professions.fetchall():
            lst_docs.append(doc[0])
            lst_symps.append([])
            symps = cur.execute(f'SELECT DISTINCT symptom FROM symptoms WHERE profession = "{doc[0]}"')
            for symp in symps.fetchall():
                lst_symps[-1].append(symp[0])

        res = dict(zip(lst_docs, lst_symps))
        return res

    #Записать информацию о пациенте в таблицу records
    def record_inf(self, id, name, phone, date, time, doc_prof, doc_name):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        time = datetime.datetime.strptime(time, '%H:%M').time()
        

        last_ticket = cur.execute('SELECT MAX(ticket) FROM records').fetchall()[0][0]
        if last_ticket is None:
            ticket = '100000000'
        else:
            ticket = str(int(last_ticket)+1)


        self.set_appointment(time, doc_name, date)
        cur.execute(f'INSERT INTO records VALUES("{id}", "{name}", "{phone}", "{date}", "{time}", "{doc_prof}", "{doc_name}", "{ticket}")')
        con.commit()

        return ticket

    #Получаем данные по id 
    def get_tickets(self, id):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        tickets = cur.execute(f'SELECT * FROM records WHERE date >= DATE("now") AND  id = "{id}"').fetchall()
        return tickets

    #Проверяем, относится ли введённый талон к пользователю (дописать!)
    def is_related_to(self, id, ticket):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        all_tickets = cur.execute(f'SELECT ticket FROM records WHERE id = "{id}"').fetchall()
        all_tickets = [t[0] for t in all_tickets]

        if ticket in all_tickets:
            return True
        else:
            return False

    #Удаляем запись пациента с records и timetable
    def delete_record(self, ticket):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        res = cur.execute(f'SELECT doc_name, date, time FROM records WHERE ticket = "{ticket}"')

        if not res:
            return None

        res = res.fetchall()
        if not res:
            return None

        data = res[0]
        doc_name = data[0]
        date = data[1]
        time = data[2]

        cur.execute(f'DELETE FROM records WHERE ticket = "{ticket}"')   
        con.commit()

        time = Database.format_time(time)
        cur.execute(f'UPDATE timetable SET "{time}" = 0 WHERE name = "{doc_name}" AND date = "{date}"')
        con.commit()

    #Получаем информацию о расписании для одного врача
    def get_timetable_by_name(self, name):
        columns = 'profession name date t9 t930 t10	t1030 t11 t1130	t12	t1230 t13 t1330	t14	t1430 t15 t1530	t16	t1630 t17 t1730	t18	t1830 t19 t1930'.split()
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        res = cur.execute(f'SELECT *  FROM timetable WHERE name = "{name}"')        

        if not res:
            return None      
        res = res.fetchall()

        return columns, res



    @staticmethod
    #hh:mm:ss -> thhmm 
    def format_time(time):
        elems = str(time).split(":")
        #Если количество часов 09, то оставляем 9 
        if elems[0][0] == '0':
            elems[0] = elems[0][1]

        if elems[1] == "00":
            res = "t{0}".format(elems[0])
        else:
            res = "t{0}{1}".format(elems[0], elems[1])

        return res