#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 22:51:55 2019

@author: password
"""
import math
def calculate_tf_idf_weights(KEYWORD_TO_URL, number_of_docs):
    for word in KEYWORD_TO_URL:
        idf = math.log10(number_of_docs/KEYWORD_TO_URL[word][0])
        for i, docs in enumerate(KEYWORD_TO_URL[word][1]):
            tf = 1 + math.log10(docs[1])
            KEYWORD_TO_URL[word][1][i][3] = tf*idf
    return KEYWORD_TO_URL

def get_tf_idf_weights(KEYWORD_TO_URL, dataframe):
    number_of_docs = len(dataframe.index)
    return calculate_tf_idf_weights(KEYWORD_TO_URL, number_of_docs)
