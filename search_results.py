#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 19:00:21 2019

@author: password
"""
from load_results import read_dictionary, read_results_sheet
from boolean_search_results import boolean_search_results
from phrase_search_results import phrase_search_results

def merge_results(boolean_results, phrase_results):
    doc_ids = set()
    bool_results = []
    for res in phrase_results:
        doc_ids.add(res[0])
    for res in boolean_results:
        if res[0] not in doc_ids:
            doc_ids.add(res[0])
            bool_results.append(res)
    phrase_results.extend(bool_results)
    return phrase_results
        

def search_query(query):
    keyword_to_urls = read_dictionary("data/keyword_to_urls.npy")
    results_data_frame = read_results_sheet("data/Results.xlsx")
    boolean_results = boolean_search_results(query, keyword_to_urls, results_data_frame)
    phrase_results = phrase_search_results(boolean_results, query)
    if phrase_results is not None:
        merged_results = merge_results(boolean_results, phrase_results)
    else:
        return boolean_results
    return merged_results

if __name__=="__main__":
    results = search_query("computer science is future")
    for res in results:
        print(res)
    