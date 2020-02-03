#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 17:53:24 2019

@author: password
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from clean_html import get_clean_words_from_html
import re
from requests.exceptions import ConnectionError, MissingSchema, HTTPError
from requests.auth import HTTPProxyAuth
import keyring
import getpass
import time
from base_url import get_base_url
from save_results import save_results
KEYWORD_TO_URL = {}
ALREADY_VISITED_URLS = {}
TEXT_OF_WEBPAGES = {}
SAVED_UPTO = -1
THRESHOLD = 50
#BASE_URL = "https://dmoz-odp.org/Computers/"

#clears the temporary dictionary of contents of webpages
def clear_text_dict():
    TEXT_OF_WEBPAGES.clear()
  
#returns clean url    
def clean_url(url):
    re.sub('\n\t', '', url)
    url = url.strip("/")
    return url

def get_auth(username = None):
    #get the username from the system if it is none
    if username is None:
        username = getpass.getuser()
    #get password if already present in the keyring
    password = keyring.get_password('credentials', username)
    #if password is not present then ask user
    if password is None:
        #get password securely
        password = getpass.getpass()
        #save/set password in keyring for future use
        keyring.set_password('credentials', username, password)
    return (username, password)

#extracts the meta description from the html soup
def get_meta_description(html_soup):
    meta_description = '' 
    #find all meta tags
    meta_tags = html_soup.find_all('meta')
    for meta_tag in meta_tags:
        tag_name = meta_tag.get('name')
        if tag_name is not None and tag_name != '':
            #if tag name is description then add its content to meta description
            if tag_name.lower()=="description":
                if meta_tag.get('content') is not None:
                    meta_description += meta_tag.get('content') + "\n"
        #get the meta tag with keywords
        tag_name = meta_tag.get('keywords')
        if tag_name is not None and tag_name != '':
            meta_description += tag_name
    #find all headings - h1, h2, h3 ...h6
    headers = html_soup.find_all(re.compile('^h[1-6]$'))
    #add the contents of all headings to meta description
    for header in headers:
        meta_description += header.text + " "
    meta_description = " ".join(meta_description.split())
    return meta_description

def get_title(html_soup):
    title = html_soup.find('title')
    if title is not None:
        title = title.text
    return title

#gets absolute url- ex - /computers will be root_url + computers, root_url - domain url
def get_absolute_next_page_url(url, next_page):
    #get the root url from the current url
    root_url = get_base_url(url)
    if next_page.startswith("/") and next_page != "/":
        next_page = root_url + next_page[1:]
    elif next_page.startswith("./") and next_page != "./":
        next_page = url + next_page[1:]
    elif not next_page.startswith("http"):
        next_page = root_url + next_page
    next_page = clean_url(next_page)
    return next_page

#maps the keywords to doc_ids (indexes of webpages)
# =============================================================================
# KEYWORD_TO_URL :- {"word"(key) -> (value)[number of docs(0), list of doc_id and other informations(1) -> [doc_id(0), no_of_times_word_appeared(1), list_of_positions(2), tf_idf(3)] ]}
# words_freq_and_pos(tells about the word and its positions in this doc) :- list of [word(0), no_of_times_word_appeared(1), positions_of_word(list of positions)]
# =============================================================================
def map_keyword_to_url(words_freq_and_pos, doc_id):
    for word in words_freq_and_pos:
        if word[0] in KEYWORD_TO_URL:
            KEYWORD_TO_URL[word[0]][1].append([doc_id, word[1], word[2], 0])
            KEYWORD_TO_URL[word[0]][0] += 1
        else:
            KEYWORD_TO_URL[word[0]] = [1, [[doc_id, word[1], word[2], 0]]]

#main crawling function, url->url currently crawling, df->dataframe of webdocs information, current_indx-> index of dataframe(will be used as doc_id), session -> session of connection, depth-> till which depth we have to crawl(default 2)
def scrap_n_crawl(url, df, current_indx, session, depth = 2):
    #if url is already visited or if depth is zero then return
    if url in ALREADY_VISITED_URLS or depth == 0:
        #increment the reference count of the url if it is already visited
        if url in ALREADY_VISITED_URLS:
            df.loc[ALREADY_VISITED_URLS[url], ['References']] += 1
        return current_indx - 1
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
            return current_indx - 1
    except MissingSchema as e:
        print(e)
        print("Invalid URL - " + url)
        return current_indx - 1
    except Exception as e:
        print(e)
        return current_indx - 1
    try:
        response.raise_for_status()
    except HTTPError as e:
        print(e)
        return current_indx - 1
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
    df.loc[current_indx] = [url, title, meta_description.replace(u'\xa0', u' '), 1]
    #store the whole clean body of webpage
    TEXT_OF_WEBPAGES[current_indx] = clean_text_body
    print(df.loc[current_indx]['Link'])
    
    ALREADY_VISITED_URLS[url] = current_indx
    
    map_keyword_to_url(words_freq_and_pos, current_indx)
    global SAVED_UPTO
    #if the number of docs that are not saved are more than the threshold value then save the data of docs first
    if (current_indx - SAVED_UPTO) >= THRESHOLD:
        save_results(KEYWORD_TO_URL, ALREADY_VISITED_URLS, TEXT_OF_WEBPAGES, df)
        clear_text_dict()
        SAVED_UPTO = current_indx
    #from here on start traversing other outgoing links
    links = html_soup.find_all('a')
    for link in links:
        next_page = link.get("href")
        if next_page is not None:
            next_page = next_page.strip()
            if next_page != '':
                if not next_page.startswith("#"):
                    next_page = get_absolute_next_page_url(url, next_page)
                    current_indx = scrap_n_crawl(next_page, df, current_indx+1, session, depth-1)
    return current_indx

if __name__=="__main__":
    if not os.path.exists('data'):
        os.makedirs('data')
        if not os.path.exists('data/doc_pages'):
            os.makedirs('data/doc_pages')
    df = pd.DataFrame(columns=['Link', 'Title', 'Meta Description', 'References'])
    session = requests.Session()
    auth = get_auth()
    session.auth = HTTPProxyAuth(auth[0], auth[1])
    session.trust_env = False
    index = scrap_n_crawl("https://dmoz-odp.org/Computers/", df, 0, session, 2)
    print("This many urls crawled: " + str(index+1))
    save_results(KEYWORD_TO_URL, ALREADY_VISITED_URLS, TEXT_OF_WEBPAGES, df)
