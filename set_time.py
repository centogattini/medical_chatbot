import sqlite3
con = sqlite3.connect('timetable.db')
cur = con.cursor()

def set_time(need_doc, need_date, time):
    res = cur.execute('UPDATE timetable SET {0} = 1 WHERE profession="{1}" AND date="2022-10-{2}"'.format(time, need_doc, need_date))
    con.commit()

set_time('Терапевт', '3', 't9')

