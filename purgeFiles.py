#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 08:05:07 2020

@author: password
"""

import os, shutil
def deleteFile(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
def delete(path):
    if os.path.exists(path):
        os.remove(path)
        
if __name__=="__main__":
    deleteFile("data/user_profiles/docid_to_clicks")
    deleteFile("data/user_profiles/user_information")
    deleteFile("data/user_profiles/user_keywords")
    deleteFile("data/group_profiles/group_information")
    deleteFile("data/group_profiles/group_keywords")
    delete("data/GRP_IDS.npy")
    delete("data/users.npy")
    delete("data/user_to_group.npy")
    