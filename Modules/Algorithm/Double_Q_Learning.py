#Imports
import random
from Modules.Algorithm.Q_Table import Q_Table
from Modules.Algorithm.Q_Learning import Q_Learning

#Class to implement Q-learning.
class Double_Q_Learning:
    
    #Constructor
    def __init__(self, table_type, move_type, alpha = 0.1, gamma = 0.6, epsilon = 0.1):
        #Create Q-Table
        self.A_q_table = Q_Table()
        self.B_q_table = Q_Table()

        #Store Q-tables in list.
        self.q_tables = [self.A_q_table, self.B_q_table]

        #Hyperparameter
        self.alpha = alpha      #Learning rate
        self.gamma = gamma      #Discount factor
        self.epsilon = epsilon   #Whether to choose a random action.

        #Table types
        self.table_type = table_type

        #Table Type 0: State: Pokemon, Action: Move
        #Table Type 1: State: Pokemon Type, Action: Move Type

        #Move types
        self.move_types = move_type

    #Methods

    #Method to select an action.
    def select_action(self, state, actions):
        #Whether to choose random actioon or not.
        if random.uniform(0,1) < self.epsilon:
            return random.choice(actions)

        else:
            #Store state-action pair not explored.
            zero_values = []

            #Store state-action pair and their Q-values.
            moves = {}

            #Loop for best action for given state.
            for action in actions:
                #Check Q-table to use.
                if self.table_type == 0:
                    #Get Q-value and check if hidden power is in action.
                    if "hiddenpower" in action._id:
                        q_value = self.q_tables[0].get_value(state, "hiddenpower") + self.q_tables[1].get_value(state, "hiddenpower")
                    else:
                        q_value = self.q_tables[0].get_value(state, action._id) + self.q_tables[1].get_value(state, action._id)
                
                elif self.table_type == 1:
                    #Get Q-value based on move type and category.

                    if str(action) == "curse (Move object)":
                        type_name = 'GHOST'
                        category_name = 'STATUS'
                    else:
                        type_name = action.type.name
                        category_name = action.category.name

                    move_info = type_name + "_" + category_name
                    q_value = self.q_tables[0].get_value(state, move_info) + self.q_tables[1].get_value(state, move_info)

                    #Check if hidden power is in action.
                    if "hiddenpower" in action._id:
                        self.move_types["hiddenpower"] = move_info
                    else:
                        #Add move info to dictionary.
                        self.move_types[action._id] = move_info

                #Update Q-value
                moves[action] = q_value

                #Check if any Q-value is 0.
                if q_value == 0:
                    zero_values.append(action)

            #print(moves)

            #Check for any 0 actions.
            if len(zero_values) != 0:
                move = random.choice(zero_values)
                return move   #Only for training!!!!!!!!!!

            else:
                move = max(moves.values())
                move = [key for key, value in moves.items() if value == move]
                move = random.choice(move)
                return move

    #Method to update Q-table
    def update_table(self, previous_state, next_state, action, reward):

        #Choose random Q-table.
        if random.uniform(0,1) < 0.5:
            update_table = 0
            other_table = 1
        else:
            update_table = 1
            other_table = 0

        #Get Q-value
        current_q = self.q_tables[update_table].get_value(previous_state, action)

        #Get max Q-value for next state.
        max_action = self.q_tables[update_table].get_arg_max(next_state)

        other_q = self.q_tables[other_table].get_value(next_state, max_action)

        #Calculate new Q-value.
        q_value = current_q + self.alpha * (reward + (self.gamma * other_q) - current_q)

        #Round Q-value.
        q_value = round(q_value, 1)

        #Update Q-Table.
        self.q_tables[update_table].update(previous_state, action, q_value)

    #Function to save the Q-table to a CSV file
    def to_CSV(self, name):
        self.A_q_table.to_CSV("A_" + name)
        self.B_q_table.to_CSV("B_" + name)

    #Function return the accumulated reward.
    def get_sum(self):
        return self.A_q_table.get_sum() + self.B_q_table.get_sum()