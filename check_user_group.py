#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 11:26:37 2019

@author: password
"""

from load_results import read_dictionary, read_list
import os
from merge_groups import findSimilarity, getCommonKeywords
from threshold import THRESHOLD
from groupCreation import createGroup
import numpy as np
from merge_groups import compareAndMerge

GRP_IDS = []
USER_TO_GRP = {}

def pre_work_grp_ids():
    global GRP_IDS
    if os.path.exists("data/GRP_IDS.npy"):
        GRP_IDS = read_list("data/GRP_IDS.npy")

def pre_work_user_to_grp():
    global USER_TO_GRP
    if os.path.exists("data/user_to_group.npy"):
        USER_TO_GRP = read_dictionary("data/user_to_group.npy")

def get_user_keywords(user_id):
    if os.path.exists(f"data/user_profiles/user_keywords/{user_id}_user_keywords.npy"):
        return read_list(f"data/user_profiles/user_keywords/{user_id}_user_keywords.npy")

def get_grp_keywords(grp_id):
    if os.path.exists(f"data/group_profiles/group_keywords/{grp_id}_group_keywords.npy"):
        return read_list(f"data/group_profiles/group_keywords/{grp_id}_group_keywords.npy")

def get_grp_data(grp_id):
    if os.path.exists(f"data/group_profiles/group_information/{grp_id}_group_data.npy"):
        return read_dictionary(f"data/group_profiles/group_information/{grp_id}_group_data.npy")

def save_grp_keywords(grp_id, grp_keywords):
    np.save(f"data/group_profiles/group_keywords/{grp_id}_group_keywords.npy", grp_keywords)
    
def save_grp_data(grp_id, grp_data):
    np.save(f"data/group_profiles/group_information/{grp_id}_group_data.npy", grp_data)

def save_user_to_grp():
    np.save("data/user_to_group.npy", USER_TO_GRP)

def updateGrpKeywords(grp_id, grp_data):
    grp_keywords = None
    user_ids = grp_data['users']
    for user_id in user_ids:
        if grp_keywords is None:
            grp_keywords = get_user_keywords(user_id)
        else:
            user_keywords = get_user_keywords(user_id)
            grp_keywords = getCommonKeywords(user_keywords, grp_keywords)
    save_grp_keywords(grp_id, grp_keywords)

def deleteGroup(grp_id):
    if os.path.exists(f"data/group_profiles/group_information/{grp_id}_group_data.npy"):
        os.remove(f"data/group_profiles/group_information/{grp_id}_group_data.npy")
    if os.path.exists(f"data/group_profiles/group_keywords/{grp_id}_group_keywords.npy"):
        os.remove(f"data/group_profiles/group_keywords/{grp_id}_group_keywords.npy")
    #GRP_IDS = read_dictionary("data/GRP_IDS.npy")
    GRP_IDS.remove(grp_id)
      
def deleteUserFromGroup(user_id, grp_id):
    grp_data = get_grp_data(grp_id)
    print(grp_data['users'])
    grp_data['users'].remove(user_id)
    if len(grp_data['users'])==0:
        deleteGroup(grp_id)
        np.save("data/GRP_IDS.npy", GRP_IDS)
        return
    updateGrpKeywords(grp_id, grp_data)
    save_grp_data(grp_id, grp_data)
        
def checkUserBelongsToGroup(user_id):
    global USER_TO_GRP
    pre_work_user_to_grp()
    pre_work_grp_ids()
    grp_id = USER_TO_GRP[user_id]
    user_keywords = get_user_keywords(user_id)
    grp_keywords = get_grp_keywords(grp_id)
    similarity = findSimilarity(user_keywords, grp_keywords)
    if similarity < THRESHOLD:
        print("checkUserBelongsToGroup, similarity < THRESHOLD, similarity: ", similarity)
        deleteUserFromGroup(user_id, grp_id)
        new_grp_id, _ = createGroup([user_id], [], user_keywords)
        print("checkUserBelongsToGroup: new_grp_id: ", new_grp_id)
        #global USER_TO_GRP
        USER_TO_GRP[user_id] = new_grp_id
        save_user_to_grp()
        compareAndMerge(new_grp_id)
    else:
        print("checkUserBelongsToGroup, similarity >= THRESHOLD, similarity: ", similarity)    
    
    
