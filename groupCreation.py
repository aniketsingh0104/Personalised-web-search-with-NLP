#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:51:13 2020

@author: password
"""
import uuid
import numpy as np
from load_results import read_list
import os

GRP_IDS = []

def pre_work():
    global GRP_IDS
    if os.path.exists("data/GRP_IDS.npy"):
        GRP_IDS = read_list("data/GRP_IDS.npy")

def save_grp(grp_id, group, keywords):
    global GRP_IDS
    np.save(f"data/group_profiles/group_information/{grp_id}_group_data.npy", group)
    np.save(f"data/group_profiles/group_keywords/{grp_id}_group_keywords.npy", keywords)
    np.save("data/GRP_IDS.npy", GRP_IDS)

def createGroup(users1, users2, keywords):
    pre_work()
    global GRP_IDS
    unique_grp_id = str(uuid.uuid4())
    users = users1
    users.extend(users2)
    group = {}
    group['group_id'] = unique_grp_id
    group['users'] = users
    GRP_IDS.append(unique_grp_id)
    save_grp(unique_grp_id, group, keywords)
    return unique_grp_id, users
