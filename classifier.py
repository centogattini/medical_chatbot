from pymorphy2 import MorphAnalyzer
from nltk import ngrams
from typing import List
import re
import json
from consts import CONST
from Levenshtein import distance 


class Classifier():

    def __init__(self, doctors_names: List[str], doctors_and_symsps: dict):
        # JSON_PATH = "data/symptoms.json"
        # try:
        #     with open(JSON_PATH, encoding='utf-8') as f:
        #         self.docs_and_symps = json.load(f)
        # except FileNotFoundError:
        #     print('Wrong path for symptoms.json')
        #     raise 
        self.doctors_and_symps = doctors_and_symsps
        for key, val in self.doctors_and_symps.items():
            self.doctors_and_symps[key] = normalize_text(val,tokenizied=True)

        self.doctors_profs = list(self.doctors_and_symps.keys())
        self.doctors_name = doctors_names
        

    def classify_symptoms(self, text) -> str:
        
        # обработка входной строки, разбиение, удаление перехода на новую строку
        # удаление знаков препинания
        tokens = normalize_text(text)
        # создание n-gram
        trigrams = ngrams(tokens, 3)
        merged_trigrams = []

        for gram in trigrams:
            merged_trigrams.append(' '.join(gram))

        bigrams = ngrams(tokens, 2)
        merged_bigrams = []
        for gram in bigrams:
            merged_bigrams.append(' '.join(gram))

        # обрабатываем все н-грамы, проверяем входение соответсвующих симптомов по врачам
        all_grams = tokens + merged_bigrams + merged_trigrams
        # вспомогательный словарь для записи количества симптомов по врачам
        doc_count = dict()
        for prof in self.doctors_profs:
            doc_count[prof] = False

        for ngram in all_grams:
            for prof in self.doctors_profs:
                if ngram in self.doctors_and_symps[prof]:
                    doc_count[prof] = True
        
        # проверяем, сколько врачей подходит
        clf_doctors = []
        for k in doc_count.keys():
            if doc_count[k] == True:
                clf_doctors.append(k)
        # если их несколько, просим обратиться к терапевту
        if len(clf_doctors) == 1:
            return clf_doctors[0], CONST.profession  # all is good
        else:
            return 'терапевт', CONST.error  # unknown sympotms

    def identify_name_or_profession(self, text):
        ans_name, ans_prof = None, None
        tokens = normalize_text(text)

        for word in tokens:
            if word in self.doctors_profs:
                ans_prof = word
                break
        
        all_grams = [' '.join(ngram) for ngram in ngrams(tokens, 3)] + \
                [' '.join(ngram) for ngram in ngrams(tokens, 2)] + tokens

        nicknames = dict()
        for full_name in self.doctors_name:
            nt = full_name.lower().split()
            nicknames[nt[0]] = full_name
            nicknames[' '.join(nt[1:])] = full_name

        for w in all_grams:
            print(w)
            if w in nicknames or w[:-1] in nicknames:
                ans_name = nicknames[w]
                break
        
        if ans_name:
            tag = CONST.name
        elif ans_prof:
            tag = CONST.profession
        else:
            tag = CONST.error

        if tag == CONST.error:
            min_dist = float('inf')
            closest = None
            for w in all_grams:
                res, d = autocorrection(w, self.doctors_profs)
                if d < min_dist:
                    closest = res
                    min_dist = d
            if min_dist <= 2:
                ans_prof = res
                tag = 'autocorr'

        return ans_name or ans_prof, tag

        # return tuple (str, tag)
        # str:string -- name or profession
        # tag: CONST variable
    
def normalize_text(text, tokenizied=False):
    morph = MorphAnalyzer()
    if tokenizied:
        text = [w.lower() for w in text]
        text = [re.sub('\\n', ' ', w) for w in text ]
        text = [re.sub('[,!.?]', '', w) for w in text]
        for i in range(len(text)):
            ws = text[i].split()
            normalized_ws = []
            for w in ws:
                normalized_ws.append(morph.parse(w)[0].normal_form)
            text[i] = ' '.join(normalized_ws)
        return text

    text = text.lower()
    text = re.sub('\\n', ' ', text)
    text = re.sub('[,!.?]', '', text)
    text = text.split(' ')
    ans = []
    for i in range(len(text)):
        ans.append(morph.parse(text[i])[0].normal_form)
    return ans


def autocorrection(word, dictionary):
    closest = None
    closest_dist = float('inf')
    for i in range(len(dictionary)):
        d = distance(word, dictionary[i])
        if d < closest_dist:
            closest = dictionary[i]
            closest_dist = d
    
    return closest, closest_dist 

    