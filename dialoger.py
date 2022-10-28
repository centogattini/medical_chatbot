from input_output import InpOut
from doctors_database import Database # hh:mm:ss
from classifier import Classifier
from consts import CONST
class Dialoger:
    def __init__(self,io:InpOut,db:Database,clf:Classifier):
        self.io = io
        self.db = db
        self.clf = clf
        self.set_of_doctors = self.db.get_all_doctors()
    # start dialog
    def start_dialog(self,):
        ans = self.ask_dyk_doctor()
        if ans == CONST.yes:
            ans = self.ask_name_or_profession()
            ans, tag = self.clf.identify_name_or_profession(ans)

            cnt = 0
            while tag == CONST.error:
                cnt += 1
                self.ask_again()
                ans = self.ask_name_or_profession()
                ans, tag = self.clf.identify_name_or_profession(ans)
                if cnt > 3:
                    break
            if tag == CONST.error:
                return
            if tag == CONST.profession:
                ans = self.ask_choose_doctor(ans)
            self.out_week()
            ans = self.ask_choose_date(ans)
            self.out_day()
            ans = self.ask_time(ans)
            self.say_bye()
        else:
            ans, tag = self.ask_symptoms()
            if tag == CONST.error:
                ans = self.ask_unknown_symptoms()
                if ans == CONST.yes:
                    ans = self.ask_choose_doctor(CONST.therapist)
                    self.out_week(ans)
                    ans = self.ask_choose_date(ans)
                    self.out_day(ans)
                    ans = self.ask_time(ans)
                    self.say_bye()
            else:
                ans = self.ask_choose_doctor()
                self.out_week(ans)
                ans = self.ask_choose_date(ans)
                self.out_day(ans)
                ans = self.ask_time(ans)
                self.say_bye()

    # tell user that we didn't understand his answer
    def ask_again(self,): 
        self.io.write('')
        pass
    # bot didn't understood symptoms and asks a person to set an apointment to therpaist
    def ask_unknown_symptoms(self,):
        pass
    # ask a person does he know the name of a doctor 
    def ask_dyk_doctor(self,)->str:
        self.io.write('Здравствуйте, вы знаете к какому доктору записаться?')
        tag = self.io.read()
        return tag
    # ask a person to write down the doctor's name
    def ask_name_or_profession(self,):
        self.io.write('Введите имя или профессию врача.')
        ans = self.io.read()
        return ans
    # ask a person to describe symptoms
    def ask_symptoms(self,):
        self.io.write('Напишите свои симптомы')
        ans = self.io.read()
        return ans
    # ask a person to choose a doctor from list of doctors
    def ask_choose_doctor(self,):
        self.io.write('Выберите специалиста')
        ans = self.io.read()
        return ans
    # output timetable for a week
    def out_week(self,ans):
        pass
    # ask a person to choose a date (from the given weekend)
    def ask_choose_date(self,ans):

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
