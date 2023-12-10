class Search:
    """Abstract class for search methods"""
    def __init__(self):
        # We will hold the number of nodes as a variable and return in the function below
        self._number_of_generated_states = 0
        self.state_utilities = {}

    def max_value(self, state, terminal_test, strategy):
        """Returns value for the max"""
        self._number_of_generated_states = 0

    def min_value(self, state, terminal_test, strategy):
        """Returns value for the min"""
        self._number_of_generated_states = 0

    def find_strategy(self, initial_state, terminal_test):
        """Applies the searching straregy"""

    def number_of_generated_states(self):
        """This function simply returns the instance member"""
        return self._number_of_generated_states
