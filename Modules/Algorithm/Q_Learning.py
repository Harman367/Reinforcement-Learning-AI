#Imports
import numpy as np
import random
from Modules.Algorithm.Q_Table import Q_Table

#Class to implement Q-learning.
class Q_Learning:
    
    #Constructor
    def __init__(self, alpha = 0.1, gamma = 0.6, epsilon = 0.1):
        #Create Q-Table
        self.q_table = Q_Table()

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
            #Store state-action pair not explored.
            zero_values = []

            moves = {}

            #Loop for best action for given state.
            for action in actions:
                #Q-value
                q_value = self.q_table.get_value(state, action._id)
                #print(action._id)

                moves[action] = q_value

                #Check if any Q-value is 0.
                if q_value == 0:
                    zero_values.append(action)


            #Check for any 0 actions.
            if len(zero_values) != 0:
                move = random.choice(zero_values)
                #print("Move choosen: " + move._id)
                return move   #Only for training!!!!!!!!!!

            else:
                move = max(moves, key = moves.get)
                #print("Move choosen: " + move._id)
                return move

    #Method to calculate reward (Q-Value)
    def get_reward(self, player, msg):
        return Reward.msg_parse(player, msg)            

    #Method to update Q-table
    def update_table(self, player, state, action, msg):
        self.q_table.update(state, action, self.get_reward(player, msg))

    #Method to update Q-table
    def update_table(self, state, action, reward):
        self.q_table.update(state, action, reward)
