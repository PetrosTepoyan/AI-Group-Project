from GameFlow import FenceChecker, MoveChecker
from GameFlow import Board, BoardTerminalTest
from Search import DLAlphaBetaSearch, MinimaxSearch, AlphaBetaSearch
from Heuristics import ShortestPathHeuristic
from Core import Player
from Actions import Move
import unittest

class DLAlphaBetaSearchTests(unittest.TestCase):
    
    def test_alpha_beta(self):
        fence_checker = FenceChecker(2, True)
        move_checker = MoveChecker()
        terminal_test = BoardTerminalTest()
        
        board = Board(
            fence_checker = fence_checker,
            move_checker = move_checker,
            grid_size = 5,
            player_positions = {
                Player.MAX : (2, 2),
                Player.MIN : (4, 4)
            },
            fences_horizontal = set(),
            fences_vertical = {(1, 3), (2, 3)}   
        )
        search = AlphaBetaSearch()
        
        strategy = search.find_strategy(board, terminal_test)
        best_action = strategy[board]
        self.assertTrue(isinstance(best_action, Move))
        self.assertEqual(strategy[board], Move((2, 2), (2, 3)))

    def test_dl_alpha_beta(self):
        fence_checker = FenceChecker(2, True)
        move_checker = MoveChecker()
        terminal_test = BoardTerminalTest()
        
        board = Board(
            fence_checker = fence_checker,
            move_checker = move_checker,
            grid_size = 5,
            player_positions = {
                Player.MAX : (2, 2),
                Player.MIN : (4, 4)
            },
            fences_horizontal = set(),
            fences_vertical = {(1, 3), (2, 3)}   
        )
        shortest_path_h = ShortestPathHeuristic()
        search = DLAlphaBetaSearch(depth = 3, heuristic = shortest_path_h)
        
        strategy = search.find_strategy(board, terminal_test)
        best_action = strategy[board]
        print(best_action)
        self.assertTrue(isinstance(best_action, Move))
        self.assertEqual(strategy[board], Move((2, 2), (2, 3)))