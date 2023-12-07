from GameFlow import Board
from Core import Player

class TerminalTest:
    def __init__(self):
        self._utilities = {}

    def utility(self, state):
        pass

    def is_terminal(self, state):
        pass

class BoardTerminalTest(TerminalTest):
    
    def is_terminal(self, board: Board):    
        max_won = board.player_positions[Player.MAX][1] >= (board.grid_size - 1)
        min_won = board.player_positions[Player.MIN][1] <= 0
        return max_won or min_won
    
    def utility(self, board: Board):
        max_won = board.player_positions[Player.MAX][1] >= (board.grid_size - 1)
        min_won = board.player_positions[Player.MIN][1] <= 0
        if max_won:
            return 1
        else:
            return -1
    