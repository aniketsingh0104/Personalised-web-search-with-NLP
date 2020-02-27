#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 18:45:22 2019

@author: password
"""
#from load_results import read_dictionary
import numpy as np

# =============================================================================
# df = pd.DataFrame([[1, 2], [4, 5], [7, 8]],columns=['max_speed', 'shield'])
# print(df)
# df.loc[0, ['shield']] += 1
# print(df)
# =============================================================================
#dic = np.load("data/group_profiles/group_information/01d112d8-5138-4201-abd7-81ec09afb9d5_group_data.npy", allow_pickle=True).tolist()
#print(dic)
def user(user_id):
    user_clicks = np.load(f"data/user_profiles/docid_to_clicks/{user_id}_docid_to_clicks.npy", allow_pickle=True)
    print("user docid to clicks: ", user_clicks)
    
    
    user_data = np.load(f"data/user_profiles/user_information/{user_id}_user_data.npy", allow_pickle=True)
    print("User data: ", user_data)
    
#    user_keywords = np.load(f"data/user_profiles/user_keywords/{user_id}_user_keywords.npy", allow_pickle=True)
#    print("User Keywords: ", user_keywords)


def group(grp_id):
    grp_data = np.load(f"data/group_profiles/group_information/{grp_id}_group_data.npy", allow_pickle=True)
    print("grp_data: ", grp_data)
    
#    grp_key = np.load(f"data/group_profiles/group_keywords/{grp_id}_group_keywords.npy", allow_pickle=True)
#    print("grp keywords: ", grp_key)

users = np.load("data/users.npy", allow_pickle=True)
print("users: ", users)

grps = np.load("data/GRP_IDS.npy", allow_pickle=True)
print("grps ", grps)

usr_grp = np.load("data/user_to_group.npy", allow_pickle=True)
print("user_grp: ", usr_grp)

group("fcc86c4c-94b3-4d91-a3aa-32fcd1d7dd26")

user("d311e1af-8941-496a-91cd-6c3bb133d123")


