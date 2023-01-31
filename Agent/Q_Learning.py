#Imports
import numpy as np
import Q_Table
import random

#Class to implement Q-learning.
class Q_Learning:
    
    #Constructor
    def __init__(self, alpha = 0.1, gamma = 0.6, epsilon = 0.1):
        #Create Q-Table
        self.q_table = Q_Table.Q_Table()

        #Hyperparameter
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon   #Whether to choose a random action.

    #Methods

    #Method to select an action.
    def select_action(self, state, actions):
        #Whether to choose random actioon or not.
        if random.uniform(0,1) < self.epsilon:
            return random.choice(actions)

        else:
            #Action to select.
            action = self.q_table.get_value(state, actions[0])

            #Store state-action pair not explored.
            zero_values = []

            #Loop for best action for given state.
            for action in actions:
                #Q-value
                q_value = self.q_table.get_value(state, action)

                #Check if any Q-value is 0.
                if q_value == 0:
                    zero_values.append(action)

                else:
                    #Find highest Q-value.
                    if action < q_value:
                        action = q_value

            #Check for any 0 actions.
            if len(zero_values) != 0:
                return random.choice(zero_values)   #Only for training!!!!!!!!!!

            else:
                return action

    #Method to calculate reward (Q-Value)
    def get_reward(self):
        pass            

    #Method to update Q-table
    def update_table(self):
        pass