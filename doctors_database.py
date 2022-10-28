import sqlite3
class Database(): 
    def __init__(self,path):
        self.table_name = 'timetable'
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
    
    def get_avaliable_time(self,name,date):
        res = self.cur.execute(f'SELECT * FROM {self.table_name} AS T WHERE T.date = "{date}" and T.name = "{name}"')
        if res is None:
            return None
        return res.fetchall()

    def set_appointment(self, time, name, date): 
        #hh:mm:ss -> thhmm   
        time = Database.format_time(time)

        try:
            self.cur.execute(f'UPDATE {self.table_name} AS T SET T.{time} = 1 WHERE T.name = {name} AND T.date = {date}')
            return 0
        except:
            return 1

    def get_all_doctors(self,):
        #set всех фио
        res = self.cur.execute(f'SELECT DISTINCT profession, name FROM {self.timetable}')
        res = set(res.fetchall())
        return res


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