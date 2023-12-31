from math import inf
from Protocols import Search
from Core import Player
from copy import deepcopy

class MinimaxSearch:
    """Classic Minimax Search"""
    def find_strategy(self, initial_state, terminal_test):
        self.state_utilities = {}
        self.visited_states = set()
        strategy = {}
        self._number_of_generated_states = 0
        self.max_value(
            deepcopy(initial_state),
            terminal_test,
            strategy
        )

        return strategy

    def max_value(self, state, terminal_test, strategy):
        if state in self.state_utilities:
            return self.state_utilities[state]

        if terminal_test.is_terminal(state):
            utility = terminal_test.utility(state)
            strategy[state] = None
            self.state_utilities[state] = utility
            return utility

        if state in self.visited_states:
            self.state_utilities[state] = 0
            return 0

        self.visited_states.add(state)

        v = -inf
        move = None

        actions = state.get_applicable_actions()

        if len(actions) == 0:
            self.state_utilities[state] = 0
            return 0

        for action in actions:
            new_state = state.get_action_result(action)
            self._number_of_generated_states += 1

            v2 = self.min_value(new_state, terminal_test, strategy)
            self.state_utilities[new_state] = v2 

            if v2 > v:
                v = v2
                move = action

            self.state_utilities[new_state] = v

        strategy[state] = move
        self.state_utilities[new_state] = v

        return v

    def min_value(self, state, terminal_test, strategy):
        if state in self.state_utilities:
            return self.state_utilities[state]

        if terminal_test.is_terminal(state):
            utility = terminal_test.utility(state)
            strategy[state] = None
            self.state_utilities[state] = utility
            return utility

        if state in self.visited_states:
            self.state_utilities[state] = 0
            return 0

        self.visited_states.add(state)

        v = inf
        move = None

        actions = state.get_applicable_actions()

        if len(actions) == 0:
            self.state_utilities[state] = 0
            return 0

        for action in actions:
            new_state = state.get_action_result(action)
            self._number_of_generated_states += 1
            v2 = self.max_value(new_state, terminal_test, strategy)
            self.state_utilities[new_state] = v2  

            if v2 < v:
                v = v2
                move = action

        strategy[state] = move
        self.state_utilities[new_state] = v

        return v
