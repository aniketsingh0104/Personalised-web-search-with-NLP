#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 18:45:22 2019

@author: password
"""
from load_results import read_dictionary

# =============================================================================
# df = pd.DataFrame([[1, 2], [4, 5], [7, 8]],columns=['max_speed', 'shield'])
# print(df)
# df.loc[0, ['shield']] += 1
# print(df)
# =============================================================================
dic = read_dictionary("data/docid_to_clicks.npy")
print(dic)
