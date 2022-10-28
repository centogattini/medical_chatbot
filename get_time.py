import sqlite3
#con = sqlite3.connect('database.db')
con = sqlite3.connect('timetable.db')
cur = con.cursor()

#Требуемый доктор и дата 
def get_time(need_doc, need_date):      
    res = cur.execute('SELECT * FROM timetable WHERE profession="{0}" AND date="2022-10-{1}"'.format(need_doc, need_date))
    return res.fetchall()[0][3:]

