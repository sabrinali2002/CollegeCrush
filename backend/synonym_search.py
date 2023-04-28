import re
import json
import statistics
from statistics import mode, StatisticsError
from urllib.error import HTTPError #special thanks: https://stackoverflow.com/questions/3193060/how-do-i-catch-a-specific-http-error-in-python
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd 


synoms_json = open('backend/synonyms.json')
#Source: https://www.kaggle.com/datasets/duketemon/wordnet-synonyms?resource=download

synom_data = json.load(synoms_json)
X1df = pd.read_csv('backend/X1_with_labels.csv')

#type(synom_data['cowboy:noun'])
parts_of_speech = ['adjective', 'adverb', 'noun', 'satellite', 'verb']
search_word = input()

if search_word in X1df.columns:
    print(X1df.nlargest(3, search_word)["University Name"])
    
for pos in parts_of_speech:
    try:
        posword = synom_data[search_word + ":" + pos].replace('|', ';')
        list_of_syms = re.split(';', posword)
        for sym in list_of_syms:
            try:
                print(X1df.nlargest(3, sym)["University Name"])
            except KeyError:
                print("no key")
            
    except KeyError:
        print("no key")
        #search for sym in idf matrix
        
    