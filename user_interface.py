#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 12:06:24 2019

@author: password
"""
from search_query import get_results
from load_results import read_results_sheet
from user_profile2 import update_user_profile
from login_or_create_user import loginUser
from check_user_group import checkUserBelongsToGroup

FINAL_RES = {}

def read_results(results, results_df):
    final_res = {}
    for res in results:
        r = results_df.iloc[res]
        #final_res.append(r)
        final_res[r[0]] = (r[1], r[2], r[3])
    return final_res
        
def show_results(results):
    results_df = read_results_sheet("data/Results.xlsx")
    global FINAL_RES
    FINAL_RES = read_results(results, results_df)
    for res in FINAL_RES:
        print(res)
        print(FINAL_RES[res][0])
        print(FINAL_RES[res][1])
        print(FINAL_RES[res][2])
        print("\n")

def take_input(user_id):
    while True:
        q = input("Enter query: ")
        if q=="":
            break
        results = get_results(q, user_id)
        show_results(results)
        inp = int(input("Enter your url id: "))
        url = FINAL_RES[inp][0]
        update_user_profile(url, user_id)
        checkUserBelongsToGroup(user_id)


def login_user():
    while True:
        username = input("Enter Username: ")
        if username!="":
            break
    user_id = loginUser(username)
    
    print("login_user: ", user_id)
    take_input(user_id)
    
if __name__=="__main__":
    login_user()
    
    