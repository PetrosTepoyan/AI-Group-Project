from GameFlow import Board, BoardTerminalTest, FenceChecker, MoveChecker
from Search import DLAlphaBetaSearch, MinimaxSearch, AlphaBetaSearch
from Core import Player
from Heuristics import ShortestPathHeuristic
from copy import deepcopy
from UIKit import UIBoard

class Versus:
    """Simulator for two bots playing against each other"""
    def __init__(self, max_depth_level: int, min_depth_level: int, grid_size: int):
        self.max_depth_level = max_depth_level
        self.min_depth_level = min_depth_level
        self.grid_size = grid_size
        
        fence_checker = FenceChecker(fence_length=2, should_check_for_obscured_path = True)
        move_checker = MoveChecker()
        self.board = Board(fence_checker, move_checker, self.grid_size)
        self.terminal_test = BoardTerminalTest()

    def start(self) -> None:
        """Begin the simulation"""
        tmp_board = deepcopy(self.board)

        heuristic = ShortestPathHeuristic()
        
        while not self.terminal_test.is_terminal(tmp_board):

            UIBoard.print_board(tmp_board)

            max_search: DLAlphaBetaSearch = DLAlphaBetaSearch(depth = self.max_depth_level, heuristic = heuristic)
            max_strategy = max_search.find_strategy(tmp_board, self.terminal_test)

            min_search: DLAlphaBetaSearch = DLAlphaBetaSearch(depth = self.min_depth_level, heuristic = heuristic)
            min_strategy = min_search.find_strategy(tmp_board, self.terminal_test)  

            if tmp_board.current_player == Player.MAX:
                max_best_action = max_strategy.get(tmp_board)
                tmp_board = tmp_board.get_action_result(max_best_action)
                continue
            else:
                min_best_action = min_strategy.get(tmp_board)
                tmp_board = tmp_board.get_action_result(min_best_action)
                continue
        

        print(self.terminal_test.utility(tmp_board))
