#!/usr/bin/env python

import numpy as np
import pandas as pd
from string import letters
from string import digits

np.random.seed(495835)

#------------------------------------------------------------------------------ 

# create names from letters and digits to create column headings


digit_let = [letter + str(digit) + letter for digit, letter in zip(digits, letters)]
let_digit = [letter + str(digit) for digit, letter in zip(digits, letters)]

letters_rand = np.random.permutation(list(letters)).tostring()
digit_rand = np.random.permutation(list(digits)).tostring()

let_digit_let = \
  [letter + str(digit) + letter1 for letter, digit, letter1 in zip(letters_rand, digit_rand, letters)]

let_let = [letter1 + letter2 for letter1, letter2 in zip(letters, letters_rand)]

# append all to digit_let list

for entry in let_digit:
    digit_let.append(entry)
    
for entry in let_digit_let:
    digit_let.append(entry)
    
for entry in let_let:
    digit_let.append(entry)

len(digit_let)


#------------------------------------------------------------------------------ 

# create a matrix

random_mtx = np.random.normal(loc = 50, scale = 1000, size = (15000, 82))

# create DataFrame

random_data_frame = pd.DataFrame(random_mtx, columns = digit_let)

random_data_frame.head()

#------------------------------------------------------------------------------ 

# create categorical labels

cat_labels = ['first', 'second', 'third', 'fourth']
part_labels = ['one', 'two']

random_data_frame['Cat'] = cat_labels * 3750
random_data_frame['Part'] = part_labels * 7500

#------------------------------------------------------------------------------ 

# export to CSV file

target_dir = '/Users/julian/GitHub/reproducible-research/extras/'
random_data_frame.to_csv(target_dir + 'common-dataset.csv', index = False)
