from calendar import c
from pymorphy2 import MorphAnalyzer
from nltk import ngrams
from collections import List
import re
import os
from consts import CONST
class Classifier():
    def __init__(self, doctors:List[str]):
        self.doctors = doctors
        pass
    def classify_symptoms(self, ans)->str:
           
        #обработка входной строки, разбиение, удаление перехода на новую строку
        #удаление знаков препинания
        morph = MorphAnalyzer()
        ans = ans.lower()
        ans = re.sub('\\n', ' ', ans)
        ans = re.sub('[,!.?]', '', ans)
        ans = ans.split(' ')
        #нормальная форма
        for i in range(len(ans)):
            ans[i] = morph.parse(ans[i])[0].normal_form
        #создание триграм, биграм
        #apfkeowkwoep
        trigrams = ngrams(ans, 3)
        merged_trigrams = []
        for gram in trigrams:
            merged_trigrams.append(' '.join(gram))

        bigrams = ngrams(ans, 2)
        merged_bigrams = []
        for gram in bigrams:
            merged_bigrams.append(' '.join(gram))
        #обрабатываем все н-грамы, проверяем входение соответсвующих симптомов по врачам
        all_grams = [ans,merged_bigrams,merged_trigrams]
        #вспомогательный словарь для записи количества симптомов по врачам
        doc_count = dict()
        for i in self.docs_and_symps.keys():
            doc_count[i] = 0
        for ngrams in all_grams:
            for ngram in ngrams:
                for k in doc_count.keys():
                    if ngram in self.docs_and_symps[k]:
                        doc_count[k] += 1
        
        #проверяем, сколько врачей подходит
        clf_doctors=[]
        for k in doc_count.keys():
            if doc_count[k] > 0:
                clf_doctors.append(k)
        #если их несколько, просим обратиться к терапевту
        if len(clf_doctors) == 1:
            return clf_doctors[0] #all is good
        else:
            return 'терапевт'#unknown sympotms
    
    def identify_name_or_profession(self,name):
        
        ans_name = None
        ans_prof = None
        doctor_names = []
        prof = []
        morph = MorphAnalyzer()
        name = re.sub('\\n', ' ', name)
        name = re.sub('[,!.?]', '', name)
        name = name.split()
        for i in range(len(name)):
            name[i] = morph.parse(name[i])[0].normal_form
        trigrams = ngrams(name, 3)

        for i in name:
            if i in prof:
                ans_prof = i
                break
        
        for i in trigrams:
            if i in doctor_names:
                ans_name = i
        
        if ans_name:
            tag = CONST.name
            return (ans_name,tag)
        elif ans_prof:
            tag = CONST.profession
            return (ans_prof,tag)
        else:
            tag = CONST.error
            return('',tag)
        # return tuple (str, tag)
        # str:string -- name or profession
        # tag: CONST variable
