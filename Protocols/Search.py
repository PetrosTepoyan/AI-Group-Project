
class Search:
    
    def __init__(self):
        # We will hold the number of nodes as a variable and return in the function below
        self._number_of_generated_states = 0
        self.state_utilities = {}
        
    def max_value(self, state, terminal_test, strategy):
        self._number_of_generated_states = 0
        pass
    
    def min_value(self, state, terminal_test, strategy):
        self._number_of_generated_states = 0
        pass
        
    def find_strategy(self, initial_state, terminal_test):
        pass
    
    # This function will simply return the instance member. 
    def number_of_generated_states(self):
        return self._number_of_generated_states