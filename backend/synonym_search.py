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

# write a function, perhaps recursive, to daisy-chain the synonyms
hits = 0
misses = 0


def find_synonym(search_word, idf_matrix=X1df, synonym_data=synom_data, min_results=1):
    if search_word in idf_matrix.columns:
        return search_word  # if word in list, no problem
    else:
        for pos in parts_of_speech:
            try:
                posword = synonym_data[search_word + ":" + pos].replace("|", ";")
                list_of_syms = re.split(
                    ";", posword
                )  # goes through the synonyms of that word
                for sym in list_of_syms:
                    try:
                        print(f"trying: {sym}")
                        if sym in idf_matrix.columns:
                            return sym
                        else:
                            return find_synonym(
                                sym, idf_matrix, synonym_data, min_results
                            )
                    except KeyError:
                        print(f"{sym} not found")
            except KeyError:
                # print(f"not in synonyms")
                x = 1
    # print("No matches found")
    return None


# def syn_list(input_list, college_word_list=test.get_words()):
#     total_list = []  # list of syn lists for all user input words
#     for word in input_list:
#         cur_list = []  # list of syns for this word
#         for pos in parts_of_speech:
#             try:
#                 posword = synom_data[word + ":" + pos].replace("|", ";")
#                 list_of_syms = re.split(";", posword)
#                 cur_list.append(list_of_syms)
#                 cur_list = cur_list.flatten()
#             except:
#                 continue
#         if word in college_word_list:
#             total_list.append([word])
#         else:
#             total_list.append(cur_list)
#     return total_list


# """
# outputs a list of (potentially new) words that are synonyms to user input words and are in our college_word_data
# """


# def intersect(syn_list, college_word_list=test.get_words()):
#     replaces = []
#     for lst in syn_list:
#         replace = set(flatten(lst)) & set(college_word_list)
#         if len(replace) != 0:
#             replaces.append(list(replace)[0])

#     return replaces


# def flatten(lst):
#     result = []
#     for item in lst:
#         if isinstance(item, list):
#             result.extend(flatten(item))
#         else:
#             result.append(item)
#     return result
