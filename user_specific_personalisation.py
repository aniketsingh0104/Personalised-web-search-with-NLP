#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 23:04:15 2019

@author: password
"""
from load_results import read_dictionary
import os

DOCID_TO_CLICKS = {}

def Sort(sub_list):
    return(sorted(sub_list, key = lambda x: x[1], reverse=True))

def pre_work(user_id):
    global DOCID_TO_CLICKS 
    if os.path.exists(f"data/user_profiles/docid_to_clicks/{user_id}_docid_to_clicks.npy"):
        DOCID_TO_CLICKS = read_dictionary(f"data/user_profiles/docid_to_clicks/{user_id}_docid_to_clicks.npy")

def get_personalised_results(results, user_id):
    pre_work(user_id)
    p_results = []
    new_raw_results = []
    #print(DOCID_TO_CLICKS)
    for res in results:
        if res[0] in DOCID_TO_CLICKS:
            p_results.append((res[0], DOCID_TO_CLICKS[res[0]]))
        else:
            new_raw_results.append(res[0])
    if len(p_results)!=0:
        p_results = Sort(p_results)   
        #print(p_results)
    return p_results, new_raw_results        