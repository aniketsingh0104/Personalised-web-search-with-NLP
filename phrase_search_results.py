#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 21:33:41 2019

@author: password
"""
from clean_html import get_stemmed_words
from nltk.corpus import stopwords
from boolean_search_results import boolean_search_results
from load_results import read_dictionary, read_results_sheet

STOPWORDS = stopwords.words('english')

def remove_stopwords(pos_of_words):
    pos_of_words = [word for word in pos_of_words if word[0] not in STOPWORDS]
    return pos_of_words

def get_pos_of_words(words):
    #pos_of_words => list of [tuple (word, i)]
    pos_of_words = [(word, i) for i, word in enumerate(words)]
    return pos_of_words

def word_pair_and_pos_diff(pos_of_words):
    #pos_diff => list of [tuple (word, next_word, difference in their position)]
    pos_diff = []
    i = 0
    while i < len(pos_of_words) - 1:
        pos_diff.append((pos_of_words[i][0], pos_of_words[i+1][0], pos_of_words[i+1][1]-pos_of_words[i][1]))
        i += 1
    return pos_diff

#match the position difference of words in query to position difference of words in docs
def matches_pos_diff(list1, list2, pos_diff):
    count = 0
    i = 0
    j = 0
    #print(list2[j]-list1[i])
    #list1 and list2 are sorted list of positions of two words
    while i<len(list1) and j<len(list2):
        diff = list2[j]-list1[i]
        if diff==pos_diff:
            count += 1
            i += 1
            j += 1
        elif diff>pos_diff:
            i += 1
        else:
            j += 1
    return count

def Sort(sub_list):
    return(sorted(sub_list, key = lambda x: (x[3], x[4], x[2], x[1]), reverse=True))

def sort_results(phrase_results):
    phrase_results = Sort(phrase_results)
    return phrase_results

# =============================================================================
# idea for getting phrase search results:
#     make pairs of words in query and find the difference in their positions from function word_pair_and_pos_diff()
#     do this for every pair of words in query and add their tf-idf wights to get final weights
#     phrase_results = list of [doc_id(0), references(1)(no_of_times_this_doc(url)_is_referenced_already_stored_in_results), tf-idf(2)(sum of all tf-idf of all word pairs found in this doc), no_of_phrases_matched(3)(how many word pairs from query actually matched), no_of_times_a_phrase_matched(4)] 
# =============================================================================
def phrase_search_results(boolean_results, query):
    docid_indx = {}
    phrase_results = []
    clean_words = get_stemmed_words(query)
    #word_freq_pos = get_word_freq_pos(clean_words)
    pos_of_words = get_pos_of_words(clean_words)
    pos_of_words = remove_stopwords(pos_of_words)
    if len(pos_of_words)<2:
        return None
    pos_diff = word_pair_and_pos_diff(pos_of_words)
    for word_pair in pos_diff:
        for result in boolean_results:
            if word_pair[0] in result[4] and word_pair[1] in result[4]:
                matches = matches_pos_diff(result[4][word_pair[0]][1], result[4][word_pair[1]][1], word_pair[2])
                if result[0] in docid_indx:
                    indx = docid_indx[result[0]]
                    if matches>0:
                        phrase_results[indx][3] += 1
                    phrase_results[indx][4] += matches
                else:
                    if matches>0:
                        phrase_results.append([result[0], result[1], result[2], 1, matches])
                    else:
                        phrase_results.append([result[0], result[1], result[2], 0, matches])
                    docid_indx[result[0]] = len(phrase_results) - 1
    phrase_results = sort_results(phrase_results)
    return phrase_results
        
if __name__=="__main__":
    keyword_to_urls = read_dictionary("data/keyword_to_urls.npy")
    results_data_frame = read_results_sheet("data/Results.xlsx")
    boolean_results = boolean_search_results("computer science is future", keyword_to_urls, results_data_frame)
    phrase_results = phrase_search_results(boolean_results, "computer science is future")
    for res in phrase_results:
        print(res)
    