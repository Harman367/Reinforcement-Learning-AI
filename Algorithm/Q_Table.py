#Imports
import numpy as np

#Class that implements the Q-Table.
class Q_Table:

    #Create Q-Table
    q_table = np.zeros(2,2)

    #Array to hold action and state for Q-Table.
    q_actions = []
    q_states = []

    #Methods

    #
    def getRow(self, state):
        if state in self.q_states:
            return self.q_states.index(state)
        else:
            self.q_states.append(state)
            return len(self.q_states) - 1

    #
    def getCol(self, action):
        pass

    #Method to update the Q-Table.
    def update(self, state, action, q_value):
        #Get row and column for Q-Table.
        row = self.q_states.get(state)
        col = self.q_actions.get(action)

        #Update Q-Value
        if row > len(self.q_table):
            pass

        if col > len(self.q_table[0]):
            pass

        self.q_table[row, col] = q_value


    #