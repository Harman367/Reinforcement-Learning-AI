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
        #Check if state is in Q-Table.
        if state in self.q_states:
            return self.q_states.index(state)
        else:
            self.q_states.append(state)
            return len(self.q_states) - 1

    #Method to return column of action in the Q-Table.
    def get_col(self, action):
        #Check if action is in Q-Table.
        if action in self.q_actions:
            return self.q_actions.index(action)
        else:
            self.q_actions.append(action)
            return len(self.q_actions) - 1

    #Method to get row and column of state and action in the Q-Table.
    def get_row_col(self, state, action):
        row = self.get_row(state)
        col = self.get_col(action)

        return row, col

    #Method to expand Q-Table.
    def expand_table(self, row, col):
        #Check if state and action is in Q-Table.
        if row >= len(self.q_table) and col >= len(self.q_table[0]):
            self.q_table = np.lib.pad(self.q_table, ((0, 1), (0, 1)), 'constant', constant_values=(0))
        
        elif row >= len(self.q_table):
            self.q_table = np.lib.pad(self.q_table, ((0, 1), (0, 0)), 'constant', constant_values=(0))

        elif col >= len(self.q_table[0]):
            self.q_table = np.lib.pad(self.q_table, ((0, 0), (0, 1)), 'constant', constant_values=(0))

    #Method to update the Q-Table.
    def update(self, state, action, q_value):
        #Get row and column for Q-Table.
        row, col = self.get_row_col(state, action)

        #Expand Q-Table if needed.
        self.expand_table(row, col)

        print("State:" + str(state) + " Action:" + str(action))
        print("Value:" + str(q_value) + " added to row: " + str(row) + " col: " + str(col))

        #Update Q-Table.
        self.q_table[row, col] = q_value

        #print(self.q_table)

    #Method to get Q-Value from Q-Table.
    def get_value(self, state, action):
        #Get row and column for Q-Table.
        row, col = self.get_row_col(state, action)
        
        #Expand Q-Table if needed.
        self.expand_table(row, col)

        #print("State: " + str(state))
        #print("Action: " + str(action) + " " + str(self.q_table[row, col]))

        return self.q_table[row, col]

    #Method to convert Q-Table to csv file.
    def to_CSV(self):
        df = pd.DataFrame(self.q_table)

        #Set column and row names.
        df.columns = self.q_actions
        df.index = self.q_states

        df.to_csv("Results/Q_Table.csv")

    #Method to load Q-Table from csv file.
    def load(self, csv):
        #Load csv file.
        df = pd.read_csv(csv, index_col = 0)

        #Get column and row names.
        self.q_actions = df.columns.values.tolist()
        self.q_states = df.index.values.tolist()

        #print(self.q_actions)
        #print(self.q_states)

        #Convert to numpy array.
        self.q_table = df.to_numpy()

        #print(self.q_table)
