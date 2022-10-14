from collections import List
from consts import CONST
class Classifier():
    def __init__(self,doctors:List[str]):
        self.doctors = doctors
        pass
    def classify_symptoms(self,)->str:
        pass
    def identify_name_or_profession(self,name):
        # return tuple (str, tag)
        # str:string -- name or profession
        # tag: CONST variable
        pass
