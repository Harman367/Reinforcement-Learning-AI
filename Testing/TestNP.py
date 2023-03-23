#Imports
import numpy as np
import pandas as pd

#Create Q-Table
q_table = np.array([[1, 2], [3, 4]])

print(q_table)

q_table = np.lib.pad(q_table, ((0, 1), (0, 2)), 'constant', constant_values=(0))

print(q_table)

import random
print(random.uniform(0, 1))