from math import inf
from copy import deepcopy
from Protocols import Search

class DLMinimaxSearch(Search):
    """Depth-Limited version of Classic Minimax Search"""
    def __init__(self, depth, heuristic):
        self.depth = depth
        self.heuristic = heuristic

    def find_strategy(self, initial_state, terminal_test):
        self.state_utilities = {}
        self.visited_states = set()
        strategy = {}
        self._number_of_generated_states = 0
        self.max_value(
            deepcopy(initial_state),
            terminal_test,
            strategy,
            self.depth
        )

        return strategy

    def max_value(self, state, terminal_test, strategy, depth):
        if state in self.state_utilities:
            return self.state_utilities[state]

        if depth == 0:
            utility = -self.heuristic(state)
            strategy[state] = None
            self.state_utilities[state] = utility
            return utility

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

            v2 = self.min_value(new_state, terminal_test, strategy, depth - 1)
            self.state_utilities[new_state] = v2 

            if v2 > v:
                v = v2
                move = action

            self.state_utilities[new_state] = v

        strategy[state] = move
        self.state_utilities[new_state] = v

        return v

    def min_value(self, state, terminal_test, strategy, depth):

        if state in self.state_utilities:
            return self.state_utilities[state]

        if depth == 0:
            utility = self.heuristic(state)
            strategy[state] = None
            self.state_utilities[state] = utility

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
            v2 = self.max_value(new_state, terminal_test, strategy, depth - 1)
            self.state_utilities[new_state] = v2  

            if v2 < v:
                v = v2
                move = action

        strategy[state] = move
        self.state_utilities[new_state] = v

        return v
