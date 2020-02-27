#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 23:04:15 2019

@author: password
"""
from load_results import read_dictionary, read_list
import os
from merge_groups import findSimilarity

DOCID_TO_CLICKS = {}

def Sort(sub_list):
    return(sorted(sub_list, key = lambda x: x[1], reverse=True))


def pre_work(user_id):
    global DOCID_TO_CLICKS 
    if os.path.exists(f"data/user_profiles/docid_to_clicks/{user_id}_docid_to_clicks.npy"):
        DOCID_TO_CLICKS = read_dictionary(f"data/user_profiles/docid_to_clicks/{user_id}_docid_to_clicks.npy")


def get_page_keywords(docID):
    doc_keywords = []
    if os.path.exists(f"data/doc_pages_keywords/{docID}.npy"):   
        doc_keywords = read_list(f"data/doc_pages_keywords/{docID}.npy")
    return doc_keywords

def groupPersonalisation(results, user_id):
    if os.path.exists("data/user_to_group.npy"):
        user_to_grp = read_dictionary("data/user_to_group.npy")
    grp_id = user_to_grp[user_id]
    if os.path.exists(f"data/group_profiles/group_keywords/{grp_id}_group_keywords.npy"):
        grp_keywords = read_list(f"data/group_profiles/group_keywords/{grp_id}_group_keywords.npy")
    grp_results = []
    for res in results:
        page_keywords = get_page_keywords(res[0])
        similarity = findSimilarity(page_keywords, grp_keywords)
        grp_results.append((res[0], similarity))
    grp_results = Sort(grp_results)
    return grp_results

def userPersonalisation(grp_results, user_id):
    pre_work(user_id)
    p_results = []
    new_raw_results = []
    # print(DOCID_TO_CLICKS)
    for res in grp_results:
        if res[0] in DOCID_TO_CLICKS:
            p_results.append((res[0], DOCID_TO_CLICKS[res[0]]))
        else:
            new_raw_results.append(res[0])
    if len(p_results) != 0:
        p_results = Sort(p_results)
    return  p_results, new_raw_results

def get_personalised_results(results, user_id):
    grp_personalisation_results = groupPersonalisation(results, user_id)
    personalisation_results, new_raw_results = userPersonalisation(grp_personalisation_results, user_id)

    return personalisation_results, new_raw_results