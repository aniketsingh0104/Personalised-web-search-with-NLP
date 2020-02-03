#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 10:33:00 2019

@author: password
"""
from search_results import search_query
from user_specific_personalisation import get_personalised_results

def merge_both_results(n_raw_results, user_personalised_results):
    final_res = []
    for res in user_personalised_results:
        final_res.append(res[0])
        #n_raw_results.append(res[0])
    final_res.extend(n_raw_results)
    return final_res
        

def get_results(query, user_id):
    raw_results = search_query(query)
    user_personalised_results, n_raw_results = get_personalised_results(raw_results, user_id)
    return merge_both_results(n_raw_results, user_personalised_results)
    
    