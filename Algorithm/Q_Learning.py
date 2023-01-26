#Imports
import numpy as np
import Q_Table

#Class to implement Q-learning.
class Q_Learning:
    
    #Create Q-Table
    q_table = Q_Table.Q_Table()

    #Hyperparameter
    alpha = 0.1
    gamma = 0.6
    epsilon = 0.1   #Whether to choose a random action.

    def select_action(actions):
        pass