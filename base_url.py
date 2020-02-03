#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 22:51:32 2019

@author: password
"""
from urllib.parse import urlparse
#returns base url, ex - https://www.digitalocean.com/xyz/jkl will return - https://www.digitalocean.com/
def get_base_url(url):
    parsed_uri = urlparse(url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    #print(result)
    return result
    
if __name__=="__main__":
    print(get_base_url('https://www.digitalocean.com'))