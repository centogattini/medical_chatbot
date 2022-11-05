import sqlite3, datetime, utils

#!!!Исправить неправильный вывод дат

#Текущая дата
curYear = datetime.datetime.now().year
curMonth = datetime.datetime.now().month
curDay = datetime.datetime.now().day

class Database():

    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
    
    #Получить время на выбранную дату по имени врача
    def get_available_time(self, name, date):
        res = self.cur.execute(f'SELECT\
            t9, t930, t10, t1030, t11, t1130, t12, t1230, t13, t1330, \
            t14, t1430, t15, t1530, t16, t1630, t17, t1730, t18, t1830, t19, t1930 \
            FROM timetable \
            AS T WHERE T.date = "{date}" AND T.name = "{name}"')

        res = utils.time_to_text(res.fetchall()[0])

        if res is None:
            return None
        return res

    #Возращает все свободные даты по имени в формате YYYY-MM-DD
    def get_date_by_name(self, name):
        #добавить от сегодняшнего дня, а не от момента создания таблицы и order by
        res = self.cur.execute(f'SELECT date FROM timetable WHERE date >= DATE("now") AND name = "{name}" AND (t9 = 0 OR t930 = 0 OR t10 = 0 OR t1030 = 0 OR t11 = 0 OR t1130 = 0 OR t12 = 0 OR t1230 = 0 OR t13 = 0 OR t1330 = 0 OR t14 = 0 OR t1430 = 0 OR t15 = 0 OR t1530 = 0 OR t16 = 0 OR t1630 = 0 OR t17 = 0 OR t1730 = 0 OR t18 = 0 OR t1830 = 0 OR t19 OR t1930) ORDER BY date ASC')
        res = res.fetchall()
        dates = []
        for i in res:
            dates.append(i[0])

        return dates

    #возращает все свободные даты по профессии в формате YYYY-MM-DD
    def get_date_by_profession(self, profession):
        res = self.cur.execute(f'SELECT date, name FROM timetable WHERE date >= DATE("now") AND profession = "{profession}" AND (t9 = 0 OR t930 = 0 OR t10 = 0 OR t1030 = 0 OR t11 = 0 OR t1130 = 0 OR t12 = 0 OR t1230 = 0 OR t13 = 0 OR t1330 = 0 OR t14 = 0 OR t1430 = 0 OR t15 = 0 OR t1530 = 0 OR t16 = 0 OR t1630 = 0 OR t17 = 0 OR t1730 = 0 OR t18 = 0 OR t1830 = 0 OR t19 OR t1930) ORDER BY date ASC')
        res = res.fetchall()
        dates = []
        for i in res:
            dates.append(i[0])

        return dates

    #Произвести запись в расписание 
    def set_appointment(self, time, name, date): 
        #hh:mm:ss -> thhmm   
        time = Database.format_time(time)
        try:
            self.cur.execute(f'UPDATE timetable AS T SET T.{time} = 1 WHERE T.name = {name} AND T.date = {date}')
            self.con.commit()
            return 0
        except:
            return 1

    #Получить множество всех врачей с именами
    def get_all_doc_n_names(self)->set:
        res = self.cur.execute(f'SELECT DISTINCT profession, name FROM timetable')
        res = set([r for r in res.fetchall()])
        return res

    #Получить множество имен всех врачей
    def get_all_names(self)->set:
        res = self.cur.execute(f'SELECT DISTINCT name FROM timetable')
        res = set([r[0] for r in res.fetchall()])
        return res

    #Получить множество всех профессии врачей 
    def get_all_professions(self)->set:
        res = self.cur.execute(f'SELECT DISTINCT profession FROM timetable')
        res = set(r[0] for r in res.fetchall())
        return res

    #Получить словарь вида {врач:симптомы}
    def get_symps_dict(self):

        professions = self.cur.execute('SELECT DISTINCT profession FROM symptoms') 
        lst_docs = []
        lst_symps = []

        for doc in professions.fetchall():
            lst_docs.append(doc[0])
            lst_symps.append([])
            symps = self.cur.execute(f'SELECT DISTINCT symptom FROM symptoms WHERE profession = "{doc[0]}"')
            for symp in symps.fetchall():
                lst_symps[-1].append(symp[0])

        res = dict(zip(lst_docs, lst_symps))
        return res

    #Записать информацию о пациенте в таблицу records
    def record_inf(self, name, phone, date, time, doc_name):

        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        time = datetime.datetime.strptime(time, '%H:%M').time()

        self.cur.execute(f'INSERT INTO records VALUES("{name}", "{phone}", "{date}", "{time}", "{doc_name}")')
        self.con.commit()

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


    @staticmethod
    def format_time(time):
        elems = time.split(":")
        #Если количество часов 09, то оставляем 9 
        if elems[0][0] == '0':
            elems[0] = elems[0][1]

        if elems[1] == "00":
            res = "t{0}".format(elems[0])
        else:
            res = "t{0}{1}".format(elems[0], elems[1])

        return res