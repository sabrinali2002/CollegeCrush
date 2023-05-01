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

#write a function, perhaps recursive, to daisy-chain the synonyms
hits = 0
misses = 0
result_univ = pd.DataFrame()
#df1.append(df2)



def search(search_word, idf_matrix, synonym_data, min_results):
    misses = 0
    global result_univ
    print(result_univ.shape[0])
    if search_word in idf_matrix.columns:
        #result_univ = pd.concat([result_univ, idf_matrix.nlargest(min_results, search_word)])
        #hits += 3
        return idf_matrix.nlargest(min_results, search_word) #if word in list, no problem
        #if result_univ.shape[0] > min_results:
        #    return result_univ
    else:
        for pos in parts_of_speech:
            try:
                posword = synonym_data[search_word + ":" + pos].replace('|', ';')
                list_of_syms = re.split(';', posword) #goes through the synonyms of that word
                for sym in list_of_syms:
                    print(f"trying: {sym}")
                    try:
                        #result_univ = pd.concat([result_univ, idf_matrix.nlargest(3, sym)]) #add these universities to our results
                        return idf_matrix.nlargest(min_results, sym) #trying with only first synom
                        print("append secondary matches")
                        #return search(sym, idf_matrix, synonym_data, min_results)
                    except KeyError: #synonym not in tf-idf matrix
                        print("Synonym not in tf-idf matrix")
                        misses += 1
                for sym in list_of_syms:
                    return search(sym, idf_matrix, synonym_data, min_results)
            except KeyError: #search word not in synonyms
                misses += 1
                print("Search Word not in synonyms dictionary")
            #search for sym in idf matrix

            #return search(search_word, idf_matrix, synonym_data, min_results)
    print("No matches found")
    return None

print((search(search_word, X1df, synom_data, 10)))
