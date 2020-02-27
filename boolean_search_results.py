#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 16:28:45 2019

@author: password
"""
from clean_html import get_stemmed_words, get_stopwords_removed
from load_results import read_dictionary, read_results_sheet

def Sort(sub_list):
    #sort the results first by total tf-idf weight and then by references
    #reverse true because we want results in decreasing order
    return(sorted(sub_list, key = lambda x: (x[2], x[1]), reverse=True))
    
def sort_results(boolean_results):
    boolean_results = Sort(boolean_results)
    return boolean_results

# =============================================================================
# =============================================================================
# # idea of getting search results -
# #   search all words of query in the keyword_to_url dict and find all the documents in which it is present
#     do this for all words and add their tf-idf weights
#     boolean_results :- list of [doc_id(0), references(1)(no_of_times_this_doc(url)_is_referenced_already_stored_in_results), tf-idf(2)(sum of all tf-idf of all words of query that are found in this doc), no_of_words_matched(3)(how many query words actually matched), dictionary of words :- {word: [no_of_times_word_appeared, list_of_positions]}] 
#     KEYWORD_TO_URL :- {"word"(key) -> (value)[number of docs(0), list of doc_id and other informations(1) -> [doc_id(0), no_of_times_word_appeared(1), list_of_positions(2), tf_idf(3)] ]}
# # =============================================================================
# 
# =============================================================================
def search_results(words, keyword_to_url, results_data_frame):
    DOCID_TO_INDEX = {}
    boolean_results = []
    #words is the list of words in query string
    for word in words:
        if word in keyword_to_url:
            #doc => [doc_id(0), no_of_times_word_appeared(1), list_of_positions(2), tf_idf(3)]
            for doc in keyword_to_url[word][1]:
                #boolean_results :- list of [doc_id(0), references(1)(no_of_times_this_doc(url)_is_referenced_already_stored_in_results), tf-idf(2)(sum of all tf-idf of all words of query that are found in this doc), no_of_words_matched(3)(how many query words actually matched), dictionary of words :- {word: [no_of_times_word_appeared, list_of_positions]}]
                if doc[0] in DOCID_TO_INDEX:
                    indx = DOCID_TO_INDEX[doc[0]]
                    boolean_results[indx][2] += doc[3]
                    boolean_results[indx][3] += 1
                    boolean_results[indx][4][word] = [doc[1], doc[2]]
                else:
                    try:
                        references = results_data_frame.loc[doc[0]]['References']
                    except Exception as e:
                        print("search_results: ", e)
                        references = 0
                    boolean_results.append([doc[0], references, doc[3], 1, {word: [doc[1], doc[2]]}])
                    DOCID_TO_INDEX[doc[0]] = len(boolean_results) - 1
    return boolean_results

def get_search_results(words, keyword_to_url, results_data_frame):
    #get the search results
    boolean_results = search_results(words, keyword_to_url, results_data_frame)
    boolean_results = sort_results(boolean_results)
    return boolean_results

def boolean_search_results(query, keyword_to_url, results_data_frame):
    #get stemmed words list from the query
    clean_words = get_stemmed_words(query)
    #remove all stopwords from the stemmed words list
    clean_words = get_stopwords_removed(clean_words)
    return get_search_results(clean_words, keyword_to_url, results_data_frame)
    
if __name__=="__main__":
    keyword_to_url = read_dictionary("data/keyword_to_urls.npy")
    results_data_frame = read_results_sheet("data/Results.xlsx")
    boolean_results = boolean_search_results("computer science is future", keyword_to_url, results_data_frame)
    for item in boolean_results:
        print(item)