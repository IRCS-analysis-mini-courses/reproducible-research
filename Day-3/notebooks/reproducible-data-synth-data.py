#!/usr/bin/env python
"""This script generates the data used
for the second homework assignment for
Day 2."""

import py_compile

py_compile.compile('reproducible-data-synth-data.py')

subj_ids = ['subj-' + str(num) for num in range(1, 103)]
groups = ['treatment-1', 'treatment-2', 'control']


import numpy as np
import pandas as pd
import os

# create group and age vectors
np.random.seed(2340875)
age_vec = np.random.uniform(low = 18, high = 52, size = len(subj_ids))

# assign subjects to an age
age_dict = {}
for subj, age in zip(subj_ids, age_vec):
	age_dict[subj] = age

# simulate correctness and RT
cols = ['Subject', 'Age', 'Group', 'Token','Attempts', 'Correct', 'RT']
sample_data = pd.DataFrame(columns = cols)
sample_data['Subject'] = subj_ids * 20 * 40
sample_data.head()

# simulate subject correctness:
# generate a DataFrame for each subject and append

# much slower than generating vector, but harder to figure out what was done

correctness = np.random.uniform(low = 0, high = 1, size = sample_data.shape[0])

for idx, prob in zip(range(sample_data.shape[0]), correctness):
	sample_data.ix[idx, 'Correct'] = np.random.binomial(n = 1, p = prob)

sample_data.head()


# assign subject reaction times:
# iterate over index, get random sample based

# generate RTs
for idx in range(sample_data.shape[0]):
	sample_data.ix[idx, 'RT'] = \
	  np.random.lognormal(mean = 6.0, sigma = 0.5) + 5 + \
	  np.random.uniform(low = 10, high = 100) + \
	  np.random.normal(loc = 70, scale = 15)
	
	
# replace values >600ms with random sample from real data
# do same for Correct column


data_dir = '~/GitHub/reproducible-research/Day-2/datasets/'
data_file = 'psycho-data-april-2015.csv'

real_data = pd.read_csv(os.path.expanduser(data_dir + data_file))

real_rt = real_data.absRT

for idx in range(sample_data.shape[0]):
	if sample_data.ix[idx, 'RT'] > 600:
		sample_data.ix[idx, 'RT'] = np.random.choice(real_rt)
	else:
		continue


# replace values > 2200 with 2200
for idx in range(sample_data.shape[0]):
	if sample_data.ix[idx, 'RT'] > 2200:
		sample_data.ix[idx, 'RT'] = 2200
	else:
		continue


sample_data.head(n = 18)

# map ages
sample_data['Age'] = sample_data.Subject.map(age_dict)
sample_data.head()


# assign counts 
for idx in range(sample_data.shape[0]):
	sample_data.ix[idx, 'Attempts'] = np.random.random_integers(low = 1, high = 15)

sample_data.head()

# assign to groups
group_dict = {}
for subj, idx in zip(subj_ids, range(1, 103)):
    if idx <= 34:
        group_dict[subj] = groups[0]
    elif idx > 34 and idx <= 68:
        group_dict[subj] = groups[2]
    elif idx > 68:
        group_dict[subj] = groups[1]

sample_data['Group'] = sample_data.Subject.map(group_dict)
sample_data.head()


sample_data = sample_data.sort(['Subject', 'Age', 'Group', 'Token'])

# change data to appropriate types
sample_data.Attempts = np.array(sample_data.Attempts, dtype = 'float64')
sample_data.Correct = np.array(sample_data.Correct, dtype = 'float64')
sample_data.RT = np.array(sample_data.RT, dtype = 'float64')

sample_data.dtypes

sample_data.head(n = 40)
sample_data.describe()

# add in trial data
# 20 trials per token

trials = range(1, 21)
sample_data['Trial'] = np.tile(trials, 40 * len(subj_ids))

# generate tokens
tokens = range(1, 21)
tokens_repeated = np.repeat(tokens, 20)
sample_data['Token'] = np.tile(tokens_repeated, 2 * len(subj_ids))
sample_data.head()


# generate phases
phases = np.repeat([1, 2], 400)
sample_data['Phase'] = np.tile(phases, 102)

sample_data.head(n = 40)

# write to csv
target_dir = '~/Github/reproducible-research/Day-2/datasets/'
filename = 'multivariate-exp-data.csv'
sample_data.to_csv(os.path.expanduser(target_dir + filename))
