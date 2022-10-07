from fcntl import DN_DELETE
import sqlite3
class Database(): 
    def __init__(self,path):
        self.table_name = 'timetable'
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
    def get_avaliable_time(self,doctor,date):
        res = self.cur.execute(f'SELECT * FROM {self.timetable} AS T WHERE T.date = "{date}" and T.doctor = "{doctor}"')
        if res is None:
            return None
        times = res.fetchone()[2:]
        return times
    def set_appointment(self,time,doctor,date): 
        self.cur.execute(f'UPDATE timtable AS T SET T.{time} = 1 WHERE T.doctor = "{doctor}" AND T.date = "{date}"')