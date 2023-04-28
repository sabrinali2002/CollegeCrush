import re
import json
import statistics
from statistics import mode, StatisticsError
from urllib.error import (
    HTTPError,
)  # special thanks: https://stackoverflow.com/questions/3193060/how-do-i-catch-a-specific-http-error-in-python
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import test

synoms_json = open("synonyms.json")
# Source: https://www.kaggle.com/datasets/duketemon/wordnet-synonyms?resource=download

synom_data = json.load(synoms_json)
X1df = pd.read_csv("X1_with_labels.csv")
parts_of_speech = ["adjective", "adverb", "noun", "satellite", "verb"]


def syn_list(input_list):
    total_list = []  # list of syn lists for all user input words
    for word in input_list:
        cur_list = []  # list of syns for this word
        for pos in parts_of_speech:
            synom_data[word + ":" + pos].replace("|", ";")
            list_of_syms = re.split(";", posword)
            cur_list.append(list_of_syms)
            cur_list = cur_list.flatten()
        total_list.append(cur_list)
        total_list = total_list.flatten()
    return total_list


"""
outputs a list of (potentially new) words that are synonyms to user input words and are in our college_word_data
"""


def intersect(syn_list, college_word_list=test.get_words()):
    replaces = []
    for lst in syn_list:
        replace = lst & college_word_list
        if replace != []:
            replaces.append(replace[0])
    assert len(replaces) == len(syn_list)
    return replaces


# type(synom_data['cowboy:noun'])


search_word = input()

if search_word in X1df.columns:
    print(X1df.nlargest(3, search_word)["University Name"])

for pos in parts_of_speech:
    try:
        posword = synom_data[search_word + ":" + pos].replace("|", ";")
        list_of_syms = re.split(";", posword)
        for sym in list_of_syms:
            try:
                print(X1df.nlargest(3, sym)["University Name"])
            except KeyError:
                print("no key")

    except KeyError:
        print("no key")
        # search for sym in idf matrix