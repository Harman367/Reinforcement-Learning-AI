#Imports
import numpy as np
import pandas as pd

#Class that implements the Q-Table.
class Q_Table:

    #Create Q-Table
    q_table = np.zeros((2,2))

    #Array to hold action and state for Q-Table.
    q_actions = []
    q_states = []

    #Methods

    #Method to return row of state in the Q-Table.
    def get_row(self, state):
        if state in self.q_states:
            return self.q_states.index(state)
        else:
            self.q_states.append(state)
            return len(self.q_states) - 1

    #Method to return column of action in the Q-Table.
    def get_col(self, action):
        #print(action)
        if action in self.q_actions:
            return self.q_actions.index(action)
        else:
            self.q_actions.append(action)
            #print(self.q_actions)
            #print(len(self.q_actions))
            return len(self.q_actions) - 1

    #Method to update the Q-Table.
    def update(self, state, action, q_value):
        #Get row and column for Q-Table.
        row = self.get_row(state)
        col = self.get_col(action)

        #Check if state and action is in Q-Table.
        if row >= len(self.q_table) and col >= len(self.q_table[0]):
            self.q_table.resize((len(self.q_table) + 1, len(self.q_table[0]) + 1))
        
        elif row >= len(self.q_table):
            self.q_table.resize((len(self.q_table) + 1, len(self.q_table[0])))

        elif col >= len(self.q_table[0]):
            self.q_table.resize((len(self.q_table), len(self.q_table[0]) + 1))

        print("Value:" + str(q_value) + " added to row: " + str(row) + " col: " + str(col))

        #Update Q-Table.
        self.q_table[row, col] = q_value

    #Method to get Q-Value from Q-Table.
    def get_value(self, state, action):
        #Get row and column for Q-Table.
        row = self.get_row(state)
        col = self.get_col(action)
        
        #Check if state and action is in Q-Table.
        if row >= len(self.q_table) and col >= len(self.q_table[0]):
            self.q_table.resize((len(self.q_table) + 1, len(self.q_table[0]) + 1))
        
        elif row >= len(self.q_table):
            self.q_table.resize((len(self.q_table) + 1, len(self.q_table[0])))

        elif col >= len(self.q_table[0]):
            self.q_table.resize((len(self.q_table), len(self.q_table[0]) + 1))
            
        #print(self.q_table)
        #print(row)
        #print(col)
        #print(len(self.q_table[0]))
        #print(self.q_actions[1])

        return self.q_table[row, col]

    #Method to convert Q-Table to csv file.
    def to_CSV(self):
        pd.DataFrame(self.q_table).to_csv("Algorithm\Q-table.csv")
