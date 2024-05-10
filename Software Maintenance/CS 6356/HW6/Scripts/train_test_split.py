#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 17:23:58 2023

@author: pritul
"""

import pandas as pd

# Load the dataset from CSV file
data = pd.read_csv('/Users/pritul/Downloads/balanced_dataset.csv')

train_ls = []

for i in range(data.shape[0]):
    if '2.0.27' in (data.iloc[i, 1]):
        train_ls.append(0)
    else:
        train_ls.append(1)

data['temp'] = train_ls

train_df = data[data['temp'] == 1]
test_df = data[data['temp'] == 0]

train_df.to_csv("/Users/pritul/Downloads/training.csv")
test_df.to_csv("/Users/pritul/Downloads/test.csv")
