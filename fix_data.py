# pip install pandas
# python fix_data.py "path_to_file"
import pandas as pd
import numpy as np
import sys

# Read csv
data = pd.read_csv(sys.argv[1], delimiter=';')

# Remove time duplicates by adding 1 to duplicates
idxs_to_increment = [-1]
while len(idxs_to_increment) > 0:
    idxs_to_increment = []
    for i in range(1, len(data)):
        if data['TIME'].at[i-1] == data['TIME'].at[i]:
            idxs_to_increment.append(i)
    for idx in idxs_to_increment:
        data.at[idx, 'TIME'] += 1

# Cut first and last two repetitions
rep_idxs = data[data['FLAG'] == 1].index
second_rep_idx = rep_idxs[1]
one_before_last_rep_idx = rep_idxs[-2]
data = data[second_rep_idx:one_before_last_rep_idx]
data = data.reset_index(drop=True)

# Make time relative to first time measured
first_time = data.at[0, 'TIME'] 
for i in range(len(data)):
    data.at[i, 'TIME'] -= first_time

# Add blank measurements to get 1000 Hz data
last_time = data['TIME'].at[len(data)-1]
curr_time_idx = 0
new_data = []
for i in range(last_time + 1):
    if data['TIME'].at[curr_time_idx] == i:
        new_data.append(data.iloc[curr_time_idx].tolist())
        curr_time_idx += 1
    else:
        new_data.append([float(0), np.nan, np.nan, np.nan, np.nan])
data = pd.DataFrame(new_data, columns=data.columns)

# Remove TIME col because now its useless
data = data.drop('TIME', axis=1)

# Interpolate missing values
data = data.interpolate()

# Sample data with 100 Hz
flag_one_idxs = data[data['FLAG'] == 1].index
for i in flag_one_idxs:
    for j in range(10):
        data.at[i + j, 'FLAG'] = 1
data = data.iloc[::10, :]

# Save to file as data.csv
data['FLAG'] = data['FLAG'].astype(int)
data.to_csv('data.csv', index=False, float_format='%.2f', header=True, sep=';')

