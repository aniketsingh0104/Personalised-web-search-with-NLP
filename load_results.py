#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 16:53:14 2019

@author: password
"""
import numpy as np
import pandas as pd

def read_dictionary(dict_path):
    dictionary = np.load(dict_path, allow_pickle=True).item()
    return dictionary

def read_results_sheet(sheet_path):
    results_dataframe = pd.read_excel(sheet_path)
    return results_dataframe