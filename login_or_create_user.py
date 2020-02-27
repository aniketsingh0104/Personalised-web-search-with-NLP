#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 22:26:41 2020

@author: password
"""
import os
from load_results import read_dictionary
import numpy as np
import uuid
from user_profile2 import save
from groupCreation import createGroup

USERS = {}
USER_KEYWORDS = []
USER_TO_GROUP = {}

def save_user_keywords(user_id):
    np.save(f"data/user_profiles/user_keywords/{user_id}_user_keywords.npy", USER_KEYWORDS)

def save_users():
    np.save('data/users.npy', USERS)

def save_user_to_group():
    np.save('data/user_to_group.npy', USER_TO_GROUP)

def pre_work():
    global USERS
    if os.path.exists("data/users.npy"):
        USERS = read_dictionary("data/users.npy")

def user_to_group():
    global USER_TO_GROUP
    if os.path.exists("data/user_to_group.npy"):
        USER_TO_GROUP = read_dictionary("data/user_to_group.npy")

def createUser(username):
    #pre_work()
    unique_id = str(uuid.uuid4())
    USERS[username] = unique_id
    save(unique_id)
    save_user_keywords(unique_id)
    save_users()
    return unique_id

def save_user_information(username, user_id, group_id):
    user = {}
    user['username'] = username
    user['user_id'] = user_id
    global USER_TO_GROUP
    USER_TO_GROUP[user_id] = group_id 
    #user['group_id'] = group_id
    np.save(f"data/user_profiles/user_information/{user_id}_user_data.npy", user)
    
def loginUser(username):
    pre_work()
    if username in USERS:
        return USERS[username]
    user_to_group()
    user_id = createUser(username)
    group_id, _ = createGroup([user_id], [], [])
    print("createGroup: group_id: ", group_id)
    save_user_information(username, user_id, group_id)
    save_user_to_group()
    return user_id


    
    