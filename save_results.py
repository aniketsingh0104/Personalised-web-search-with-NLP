#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 00:00:45 2019

@author: password
"""
from tf_idf import get_tf_idf_weights
import numpy as np
import zlib
from webpagesKeywords import getAndSaveKeywords

def Sort(sub_list):
    return(sorted(sub_list, key = lambda x: x[3], reverse=True))

def sort_results(KEYWORD_TO_URL):
    for keyword in KEYWORD_TO_URL:
        KEYWORD_TO_URL[keyword][1] = Sort(KEYWORD_TO_URL[keyword][1])
    return KEYWORD_TO_URL

def save_results(KEYWORD_TO_URL, ALREADY_VISITED_URLS, TEXT_OF_WEBPAGES, df):
    KEYWORD_TO_URL = get_tf_idf_weights(KEYWORD_TO_URL, df)
    KEYWORD_TO_URL = sort_results(KEYWORD_TO_URL)
    df.to_excel("data/Results.xlsx")
    np.save('data/keyword_to_urls.npy', KEYWORD_TO_URL)
    np.save('data/already_visited_urls.npy', ALREADY_VISITED_URLS)
    for doc_id in TEXT_OF_WEBPAGES:
        compressed_data = zlib.compress(bytearray(TEXT_OF_WEBPAGES[doc_id], 'utf-8'))
        with open(f'data/doc_pages/{doc_id}.zlib', 'wb') as fp:
            fp.write(compressed_data)
        getAndSaveKeywords(TEXT_OF_WEBPAGES[doc_id], doc_id)
    
