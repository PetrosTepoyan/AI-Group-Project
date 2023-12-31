from copy import deepcopy
from math import inf
from Protocols import Search
from Core import Player
from UIKit import UIBoard

class DLAlphaBetaSearch(Search):
    """Depth-Limited version of Classic Alpha-Beta Search"""
    def __init__(self, depth, heuristic, visit_count = {}):
        self.depth = depth
        self.heuristic = heuristic
        self.visit_count = visit_count

    def find_strategy(self, initial_state, terminal_test):
        strategy = {}
        self.state_utilities = {}
        self.visited_states = set()
        self._number_of_generated_states = 0
        root_function = self.max_value if initial_state.current_player is Player.MAX else self.min_value
        root_function(
            deepcopy(initial_state),
            terminal_test,
            -inf, inf,
            strategy,
            self.depth
        )
        return strategy

    def max_value(self, state, terminal_test, alpha, beta, strategy, depth):
        # UIBoard.print_board(state)
        if state in self.state_utilities:
            return self.state_utilities[state]

        if depth == 0 or terminal_test.is_terminal(state):
            utility = self.heuristic(state)
            strategy[state] = None
            self.state_utilities[state] = utility
            return utility
        
        if self.visit_count.get(state):
            self.visit_count[state] += 1
        else:
            self.visit_count[state] = 0
        
        if self.visit_count.get(state) > 0:
            return 0

        # The advantages of alpha-beta start to arise here.
        # We first make a symbolical reassignment of alpha
        alpha_1 = alpha
        v = -inf
        move = None

        actions = state.get_applicable_actions()

        if len(actions) == 0:
            self.state_utilities[state] = 0
            return 0

        for action in actions:
            new_state = state.get_action_result(action)
            self._number_of_generated_states += 1
            v2 = self.min_value(new_state, terminal_test, alpha_1, beta, strategy, depth - 1)

            if v2 > v:
                v = v2
                move = action
                # Here, we update the value of alpha if we found a greater one
                alpha_1 = max(alpha_1, v)

            # And here is the power of alpha-beta. If we found that our current
            # utility is greater than beta, we will simply return the utility, thus
            # pruning the other states.
            if v > beta:
                strategy[state] = move
                self.state_utilities[new_state] = v
                return v

        strategy[state] = move
        self.state_utilities[new_state] = v

        if move is not None:
            strategy[state] = move

        return v

    # Analogically to the method above, we implement min_value method
    def min_value(self, state, terminal_test, alpha, beta, strategy, depth):
        # UIBoard.print_board(state)
        if state in self.state_utilities:
            return self.state_utilities[state]

        if depth == 0 or terminal_test.is_terminal(state):
            utility = -self.heuristic(state)
            strategy[state] = None
            self.state_utilities[state] = utility
            return utility
        
        if self.visit_count.get(state):
            self.visit_count[state] += 1
        else:
            self.visit_count[state] = 0
        
        if self.visit_count.get(state) > 0:
            return 0
        
        v = inf
        beta_1 = beta
        move = None

        actions = state.get_applicable_actions()

        if len(actions) == 0:
            self.state_utilities[state] = 0
            return 0

        for action in actions:
            new_state = state.get_action_result(action)
            self._number_of_generated_states += 1
            v2 = self.max_value(new_state, terminal_test, alpha, beta_1, strategy, depth - 1)

            if v2 < v:
                v = v2
                move = action
                beta_1 = min(beta_1, v)

            if v < alpha:
                strategy[state] = move
                self.state_utilities[new_state] = v
                return v

        if move is not None:
            strategy[state] = move

        self.state_utilities[new_state] = v

        return v
