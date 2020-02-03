#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 17:58:32 2019

@author: password
"""
from bs4 import Comment
import nltk
from nltk.stem import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
STOPWORDS = stopwords.words('english')
SNOWBALL_STEMMER = SnowballStemmer('english')

#remove all stopwords from a list of words
def get_stopwords_removed(words):
    clean_words = [word for word in words if word not in STOPWORDS]
    return clean_words

#tokenize and perform stemming then return the list of stemmed words
def get_stemmed_words(text):
    clean_words = []
    #break the text into sentences
    sentences = nltk.sent_tokenize(text)
    tokenizer = RegexpTokenizer(r'\w+')
    for sentence in sentences:
        #tokenize each sentence
        word_tokens = tokenizer.tokenize(sentence)
        #perform stemming on each word and return stemmed words
        stemmed_words = [SNOWBALL_STEMMER.stem(word) for word in word_tokens]
# =============================================================================
#         for word in stemmed_words:
#             print(word)
# =============================================================================
# =============================================================================
#         clean_word_list = [word for word in stemmed_words if word not in STOPWORDS]
#         clean_word_list = Counter(stemmed_words)
#         print(clean_word_list)
#         clean_words = list(set(clean_words).union(stemmed_words))
# =============================================================================
        clean_words.extend(stemmed_words)
    return clean_words
#words_freq_and_pos(tells about the word and its positions in this words list) :- list of [word(0), no_of_times_word_appeared(1), positions_of_word(list of positions)(2)]
def get_word_freq_pos(clean_words):
    #this dictionary will maintain the positions against each word
    words_pos = {}
    for i, word in enumerate(clean_words):
        words_pos.setdefault(word, []).append(i)
    words_freq_and_pos = [(word, len(words_pos[word]), words_pos[word]) for word in words_pos]
    return words_freq_and_pos

def get_clean_words(text):
    clean_words = get_stemmed_words(text)
    
# =============================================================================
#     for word in clean_words_and_freq:
#         print(word, clean_words_and_freq[word])
# =============================================================================
# =============================================================================
#     for word in words_freq_and_pos:
#         print(word)
# =============================================================================
    return get_word_freq_pos(clean_words)

def get_clean_html(soup):
    #kill all script and style elements
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    for script in soup(["script", "style"]):
        script.extract()
    #get text
    text = soup.get_text()
    #break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    #break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    #drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def get_clean_words_from_html(soup):
    text = get_clean_html(soup)
    return get_clean_words(text), text

if __name__=="__main__":
    get_clean_words("This is a Demo Text for NLP using NLTK. This Demo is shown for Text cleaning using NLTK.")
    clean_words = get_stemmed_words("computer science is future")
    clean_words = get_stopwords_removed(clean_words)
    for word in clean_words:
        print(word)