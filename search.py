from math import inf
from Protocols import Search
from Core import Player

class MinimaxSearch(Search):
    
    def find_strategy(self, initial_state, terminal_test):
        self.state_utilities = {}
        self.visited_states = set()
        strategy = {}
        self._number_of_generated_states = 0
        self.max_value(initial_state, terminal_test, strategy)
        
        return strategy

    def max_value(self, state, terminal_test, strategy):
        # We check if it is the optimized version that we are calling. If yes, we keep (state, utility) pairs
        if state in self.state_utilities:
            return self.state_utilities[state]
        
        # Check for the terminal state. If it is, we store the utility and return it
        if terminal_test.is_terminal(state):
            utility = terminal_test.utility(state)
            strategy[state] = None
            self.state_utilities[state] = utility
            return utility
        
        # Explanation can be found from the pseudocode
        v = -inf
        move = None
        # Loop through available actions
        actions = state.get_applicable_actions()
        # print(len(actions), len(state.fences_horizontal), len(state.fences_vertical))
        # print(len(actions), state.player_positions[Player.MAX], state.player_positions[Player.MIN])
        for action in actions:
            # Generate new state and increment the number of generated states
            new_state = state.get_action_result(action)
            self._number_of_generated_states += 1
            
            if new_state in self.visited_states:
                # print("repeated state", new_state)
                self.state_utilities[new_state] = 0
                continue
            
            self.visited_states.add(new_state)
            
            # Recursive call to min_value
            v2 = self.min_value(new_state, terminal_test, strategy)
            
            # If we found a utility greater than the current one, we update it as well as the action
            if v2 > v:
                v = v2
                move = action
                
            self.state_utilities[new_state] = v
        
        # At the end we store the pairs (state, action) and (state, utility)
        strategy[state] = move
        self.state_utilities[new_state] = v
        
        return v
    
    # Implementation and the explanation is nearly identical to the one above.
    def min_value(self, state, terminal_test, strategy):
        if state in self.state_utilities:
            return self.state_utilities[state]
        
        if terminal_test.is_terminal(state):
            utility = terminal_test.utility(state)
            strategy[state] = None
            self.state_utilities[state] = utility
            return utility
            
        v = inf
        move = None
        
        actions = state.get_applicable_actions()

        # print("How many actions", len(actions))
        # print("MIN_VALUE")
        # print(len(actions), state.player_positions[Player.MAX], state.player_positions[Player.MIN])
        for action in actions:
            new_state = state.get_action_result(action)
            self._number_of_generated_states += 1
            
            if new_state in self.visited_states:
                # print("repeated state", new_state)
                self.state_utilities[new_state] = 0
                continue
            
            self.visited_states.add(new_state)
            
            v2 = self.max_value(new_state, terminal_test, strategy)
            if v2 < v:
                v = v2
                move = action
        
        strategy[state] = move
        self.state_utilities[new_state] = v  
        
        return v

class AlphaBetaSearch(Search):
    
    def find_strategy(self, initial_state, terminal_test):
        strategy = {}
        self.state_utilities = {}
        self._number_of_generated_states = 0
        self.max_value(initial_state, terminal_test, -inf, inf, strategy)
        return strategy

    def max_value(self, state, terminal_test, alpha, beta, strategy):
        
        if state in self.state_utilities:
            return self.state_utilities[state]
        
        if terminal_test.is_terminal(state):
            utility = terminal_test.utility(state)
            strategy[state] = None
            self.state_utilities[state] = utility
            return utility
        
        # The advantages of alpha-beta start to arise here. We first make a symbolical reassignment of alpha
        alpha_1 = alpha
        v = -inf
        move = None
        
        actions = state.get_applicable_actions()
        for action in actions:
            new_state = state.get_action_result(action)
            self._number_of_generated_states += 1
            v2 = self.min_value(new_state, terminal_test, alpha_1, beta, strategy)
            
            if v2 > v:
                v = v2
                move = action
                # Here, we update the value of alpha if we found a greater one
                alpha_1 = max(alpha_1, v)
                
            # And here is the power of alpha-beta. If we found that our current utility is greater than beta,
            # We will simply return the utility, thus pruning the other states.
            if v >= beta:
                strategy[state] = move
                self.state_utilities[new_state] = v
                return v
        
        strategy[state] = move.prev_turn
        self.state_utilities[new_state] = v
        
        return v
    
    # Analogically to the method above, we implement min_value method
    def min_value(self, state, terminal_test, alpha, beta, strategy):
        
        if state in self.state_utilities:
            return self.state_utilities[state]
        
        if terminal_test.is_terminal(state):
            utility = terminal_test.utility(state)
            strategy[state] = None
            self.state_utilities[state] = utility
            return utility
        
        v = inf
        beta_1 = beta
        move = None
        
        actions = state.get_applicable_actions()

        for action in actions:
            new_state = state.get_action_result(action)
            self._number_of_generated_states += 1
            v2 = self.max_value(new_state, terminal_test, alpha, beta_1, strategy)
            
            if v2 < v:
                v = v2
                move = action
                beta_1 = min(beta_1, v)
                
            if v <= alpha:
                strategy[state] = move
                self.state_utilities[new_state] = v  
        
                return v
                
            
        strategy[state] = move.prev_turn
        self.state_utilities[new_state] = v  
        
        return v