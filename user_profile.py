#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 11:26:37 2019

@author: password
"""
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, MissingSchema, HTTPError
from requests.auth import HTTPProxyAuth
import time
import pandas as pd
from crawl_and_scrap import get_auth, get_title, get_meta_description, clean_url
import os
from load_results import read_dictionary, read_results_sheet
from clean_html import get_clean_words_from_html
from save_results import save_UP_results

#from crawl_and_scrap import scarp_and_crawl
ALREADY_VISITED_URLS = {}
KEYWORD_TO_URL = {}
TEXT_OF_WEBPAGES = {}

def clear_text_dict():
    TEXT_OF_WEBPAGES.clear()

def map_keyword_to_url(words_freq_and_pos, doc_id):
    for word in words_freq_and_pos:
        if word[0] in KEYWORD_TO_URL:
            KEYWORD_TO_URL[word[0]][1].append([doc_id, word[1], word[2], 0])
            KEYWORD_TO_URL[word[0]][0] += 1
        else:
            KEYWORD_TO_URL[word[0]] = [1, [[doc_id, word[1], word[2], 0]]]

def pre_work():
    if os.path.exists("data/UP_results.xlsx"):
        df = read_results_sheet("data/UP_results.xlsx") 
        global ALREADY_VISITED_URLS, KEYWORD_TO_URL
        ALREADY_VISITED_URLS = read_dictionary("data/UP_already_visited_urls.npy")
        KEYWORD_TO_URL = read_dictionary("data/UP_keyword_to_urls.npy")
    else:
        df = pd.DataFrame(columns=['Link', 'Title', 'Meta Description', 'Clicks'])
    session = requests.Session()
    auth = get_auth()
    session.auth = HTTPProxyAuth(auth[0], auth[1])
    session.trust_env = False
    return session, df

def update(url, df, session):
    if url in ALREADY_VISITED_URLS:
        df.loc[ALREADY_VISITED_URLS[url], ['Clicks']] += 1
        return
    indx = df.shape[0]
    try:
        #get the response of the url
        response = session.get(url)
    except ConnectionError as e:
        #if url blocks you then wait for some time and again try
        print(e)
        time.sleep(2)
        try:
            response = session.get(url)
        except:
            return
    except MissingSchema as e:
        print(e)
        print("Invalid URL - " + url)
        return 
    except Exception as e:
        print(e)
        return
    try:
        response.raise_for_status()
    except HTTPError as e:
        print(e)
        return 
    #get the raw text of response
    raw_text = response.text
    #parse the raw text with html parser of beautifulSoup
    html_soup = BeautifulSoup(raw_text, "html.parser")
    #get the words_freq_and_pos and clean_text from html soup
    words_freq_and_pos, clean_text_body = get_clean_words_from_html(html_soup)
    title = get_title(html_soup)
    meta_description = get_meta_description(html_soup)
    #get clean url with removed unnecessary slashes
    url = clean_url(url)
    #store the document(webpage) details, last feild is of reference
    df.loc[indx] = [url, title, meta_description.replace(u'\xa0', u' '), 1]
    #store the whole clean body of webpage
    TEXT_OF_WEBPAGES[indx] = clean_text_body
    ALREADY_VISITED_URLS[url] = indx
    
    map_keyword_to_url(words_freq_and_pos, indx)
    save_UP_results(KEYWORD_TO_URL, ALREADY_VISITED_URLS, TEXT_OF_WEBPAGES, df)
    clear_text_dict()
    return
    
def update_user_profile(url):
    session, df = pre_work()
    update(url, df, session)
    
if __name__=="__main__":
    session, df = pre_work()
        
