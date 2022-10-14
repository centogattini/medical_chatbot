from input_output import InpOut
from doctors_database import Database
class Dialog:
    def __init__(self,io:InpOut,db:Database):
        self.io = io
        self.db = db
    # ask a person does he know the name of a doctor 
    def ask_dyk_doctor(self,):
        pass
    # ask a person to write down the doctor's name
    def ask_name_or_profession(self,):
        pass
    # ask a person to describe symptoms
    def ask_symptoms(self,):
        pass
    # ask a person to choose a doctor from list of doctors
    def ask_choose_doctor(self,):
        pass
    # output timetable for a week
    def out_week(self,):
        pass
    # ask a person to choose a date (from the given weekend)
    def ask_choose_date(self,):
        pass
    # output timetable for a day
    def out_day(self,):
        pass
    # ask a person to choose time for a visit
    def ask_time(self,):
        pass
    # say bye
    def say_bye(self,):
        pass
