#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 19:32:16 2020

@author: password
"""
from clean_html import get_stemmed_words
import numpy as np
from os import listdir
from os.path import isfile, join, splitext
import zlib

MYPATH = "data/doc_pages"

def getKeywordsFromCompressedFiles():
    for f in listdir(MYPATH):
        if isfile(join(MYPATH, f)):
            with open(join(MYPATH, f), 'rb') as fp:
                compressed_data = fp.read()
                decompressed_data = zlib.decompress(compressed_data)
                pageData = decompressed_data.decode('utf-8')
                getAndSaveKeywords(pageData, splitext(f)[0])
                #print(page_keywords)
            

def getAndSaveKeywords(pageData, page_id):
    words = get_stemmed_words(pageData)
    np.save(f"data/doc_pages_keywords/{page_id}.npy",words)
    return words
    
if __name__=="__main__":
#    with open("data/doc_pages/1.zlib", 'rb') as fp:
#        compressed_data = fp.read()
#        decompressed_data = zlib.decompress(compressed_data)
#        print(decompressed_data)
    getKeywordsFromCompressedFiles()
    