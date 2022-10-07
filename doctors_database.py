
import sqlite3
class Database(): 
    def __init__(self,path):
        self.table_name = 'timetable'
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
    def get_avaliable_time(self,profession,date):
        res = self.cur.execute(f'SELECT * FROM {self.timetable} AS T WHERE T.date = "{date}" and T.profession = "{profession}"')
        if res is None:
            return None
        return res.fetchone()
    def set_appointment(self,time,profession,date): 
        self.cur.execute(f'UPDATE timtable AS T SET T.{time} = 1 WHERE T.profession = "{profession}" AND T.date = "{date}"')
    def get_all_doctors(self,):
        res = self.cur.execute(f'SELECT DISTINCT T.profession, T.name FROM timetable')
        return res.fetchone()