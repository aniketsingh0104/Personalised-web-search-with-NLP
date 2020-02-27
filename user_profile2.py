#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 21:29:47 2019

@author: password
"""
import os
from load_results import read_dictionary, read_list
from crawl_and_scrap import clean_url
import numpy as np

DOCID_TO_CLICKS = {}
URL_TO_DOCIDS = {}
USER_KEYWORDS = []

def save_user_keywords(user_id):
    np.save(f"data/user_profiles/user_keywords/{user_id}_user_keywords.npy", USER_KEYWORDS)

def save(user_id):
    np.save(f'data/user_profiles/docid_to_clicks/{user_id}_docid_to_clicks.npy', DOCID_TO_CLICKS)

def pre_work(user_id):
    global DOCID_TO_CLICKS, URL_TO_DOCIDS, USER_KEYWORDS
    if os.path.exists(f"data/user_profiles/docid_to_clicks/{user_id}_docid_to_clicks.npy"):
        DOCID_TO_CLICKS = read_dictionary(f"data/user_profiles/docid_to_clicks/{user_id}_docid_to_clicks.npy")
    if os.path.exists("data/already_visited_urls.npy"):
        URL_TO_DOCIDS = read_dictionary("data/already_visited_urls.npy")
    if os.path.exists(f"data/user_profiles/user_keywords/{user_id}_user_keywords.npy"):
        USER_KEYWORDS = read_list(f"data/user_profiles/user_keywords/{user_id}_user_keywords.npy")

def get_doc_keywords(doc_id):
    keywords = []
    if os.path.exists(f"data/doc_pages_keywords/{doc_id}.npy"):
        keywords = read_list(f"data/doc_pages_keywords/{doc_id}.npy")
    return keywords

def extend_user_keywords(doc_keywords):
    global USER_KEYWORDS
    USER_KEYWORDS.extend(doc_keywords)
    

def update_user_profile(url, user_id):
    pre_work(user_id)
    url = clean_url(url)
    if url in URL_TO_DOCIDS:
        doc_id = URL_TO_DOCIDS[url]
        if doc_id in DOCID_TO_CLICKS:
            DOCID_TO_CLICKS[doc_id] += 1
        else:
            DOCID_TO_CLICKS[doc_id] = 1
        doc_keywords = get_doc_keywords(doc_id)
        extend_user_keywords(doc_keywords)
        save_user_keywords(user_id)
        save(user_id)
    
    