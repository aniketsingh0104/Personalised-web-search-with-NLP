#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 22:33:13 2020

@author: password
"""
from collections import Counter
from groupCreation import createGroup
from load_results import read_dictionary, read_list
import numpy as np
import os
from threshold import THRESHOLD

GRP_IDS = []

def pre_work():
    global GRP_IDS
    if os.path.exists("data/GRP_IDS.npy"):
        GRP_IDS = read_list("data/GRP_IDS.npy")

def findSimilarity(keywords1, keywords2):
    words1_vals = Counter(keywords1)
    words2_vals = Counter(keywords2)
    
    words = list(words1_vals.keys() | words2_vals.keys())
    words1_vect = [words1_vals.get(word, 0) for word in words]
    words2_vect = [words2_vals.get(word, 0) for word in words]
    
    len_words1  = sum(av*av for av in words1_vect) ** 0.5
    len_words2  = sum(bv*bv for bv in words2_vect) ** 0.5
    dot    = sum(av*bv for av,bv in zip(words1_vect, words2_vect))
    if(len_words1==0 or len_words2==0):
        return 0
    cosine = dot / (len_words1 * len_words2)  
    return cosine

def getCommonKeywords(group1_keywords, group2_keywords):
    common_keywords = [word for word in group1_keywords if word in group2_keywords]
    return common_keywords

def updateUsersWithNewGroup(users, grp_id):
    user_to_group = read_dictionary("data/user_to_group.npy")
    for user_id in users:
        user_to_group[user_id] = grp_id
    np.save("data/user_to_group.npy", user_to_group)
        
def deleteGroup(grp_id):
    if os.path.exists(f"data/group_profiles/group_information/{grp_id}_group_data.npy"):
        os.remove(f"data/group_profiles/group_information/{grp_id}_group_data.npy")
    if os.path.exists(f"data/group_profiles/group_keywords/{grp_id}_group_keywords.npy"):
        os.remove(f"data/group_profiles/group_keywords/{grp_id}_group_keywords.npy")
    #GRP_IDS = read_dictionary("data/GRP_IDS.npy")
    GRP_IDS.remove(grp_id)

def mergeTwoGroups(group1_data, group1_keywords, group2_data, group2_keywords):
    common_keywords = getCommonKeywords(group1_keywords, group2_keywords)
    new_grpid, users = createGroup(group1_data['users'], group2_data['users'], common_keywords)
    print("mergeTwoGroups: new group id: ", new_grpid)
    updateUsersWithNewGroup(users, new_grpid)
    print("mergeTwoGroups: group1_id: ", group1_data['group_id'])
    deleteGroup(group1_data['group_id'])
    print("mergeTwoGroups: group2_id: ", group2_data['group_id'])
    deleteGroup(group2_data['group_id'])

def compareAndMerge(grp_id):
    pre_work()
    grp2_id = None
    grp2_keywords = None
    max_match = 0
    print("compareAndMerge: ", grp_id)
    group1_keywords = read_list(f"data/group_profiles/group_keywords/{grp_id}_group_keywords.npy")
    for g_id in GRP_IDS:
        if g_id != grp_id:
            group2_keywords = read_list(f"data/group_profiles/group_keywords/{g_id}_group_keywords.npy")
            similarity = findSimilarity(group1_keywords, group2_keywords)
            if similarity>=THRESHOLD:
                if similarity>max_match:
                    max_match = similarity
                    grp2_id = g_id
                    grp2_keywords = group2_keywords
    if grp2_id is not None:
        group1_data = read_dictionary(f"data/group_profiles/group_information/{grp_id}_group_data.npy")
        group2_data = read_dictionary(f"data/group_profiles/group_information/{grp2_id}_group_data.npy")
        mergeTwoGroups(group1_data, group1_keywords, group2_data, grp2_keywords)

if __name__=="__main__":
    print(findSimilarity(['apple', 'crap', 'sigmjj', 'hello'], ['apple', 'crap', 'gmjj', 'llo']))