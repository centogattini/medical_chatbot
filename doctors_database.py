import sqlite3
class Database():


    def __init__(self,path):
        self.table_name = 'timetable'
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
    
    #Получить время по имени и дате
    def get_available_time(self,name,date):
        res = self.cur.execute(f'SELECT\
            t9, t930, t10, t1030, t11, t1130, t12, t1230, t13, t1330, \
            t14, t1430, t15, t1530, t16, t1630, t17, t1730, t18, t1830 \
            FROM {self.table_name} \
            AS T WHERE T.date = "{date}" and T.name = "{name}"')
        if res is None:
            return None
        return res.fetchall()

    #возращает свободные даты по имени на неделю
    def get_available_date(self, name):
        res = self.cur.execute(f'SELECT date FROM timetable WHERE name = "{name}" AND (t9 = 0 OR t930 = 0 OR t10 = 0 OR t1030 = 0 OR t11 = 0 OR t1130 = 0 OR t12 = 0 OR t1230 = 0 OR t13 = 0 OR t1330 = 0 OR t14 = 0 OR t1430 = 0 OR t15 = 0 OR t1530 = 0 OR t16 = 0 OR t1630 = 0 OR t17 = 0 OR t1730 = 0 OR t18 = 0 OR t1830 = 0)')
        res = res.fetchmany(7)
        dates = []
        for i in res:
            dates.append(i[0])

        return dates


    #Произвести запись в расписание 
    def set_appointment(self, time, name, date): 
        #hh:mm:ss -> thhmm   
        time = Database.format_time(time)

        try:
            self.cur.execute(f'UPDATE {self.table_name} AS T SET T.{time} = 1 WHERE T.name = {name} AND T.date = {date}')
            return 0
        except:
            return 1

    #Получить имена всех врачей
    def get_all_doctors(self,):
        res = self.cur.execute(f'SELECT DISTINCT profession, name FROM {self.timetable}')
        res = set(res.fetchall())
        return res

    #Получить все профессии врачей
    def get_all_professions(self,):
        #set всех профессий 
        res = self.cur.execute(f'SELECT DISTINCT profession FROM {self.timetable}')
        res = set(res.fetchall())
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