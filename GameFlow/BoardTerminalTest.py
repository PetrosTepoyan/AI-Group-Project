from GameFlow import Board
from Core import Player
from Protocols import TerminalTest

class BoardTerminalTest(TerminalTest):
    """A `TerminalTest` utility function that checks if Quoridor state is terminal"""
    def is_terminal(self, state: Board) -> bool:
        max_won = state.player_positions[Player.MAX][1] >= (state.move_checker.grid_size - 1)
        min_won = state.player_positions[Player.MIN][1] <= 0
        return max_won or min_won

    def utility(self, state: Board) -> int:
        max_won = state.player_positions[Player.MAX][1] >= (state.move_checker.grid_size - 1)
        min_won = state.player_positions[Player.MIN][1] <= 0
        if max_won:
            return 1
        if min_won:
            return -1
        return 0
    