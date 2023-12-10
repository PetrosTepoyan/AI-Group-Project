import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from GameFlow import FenceChecker, MoveChecker
from GameFlow import Board, BoardTerminalTest
from Search import DLAlphaBetaSearch, MinimaxSearch, AlphaBetaSearch
from Heuristics import ShortestPathHeuristic
from Core import Player
from Actions import Move, PlaceFence
import unittest
from UIKit import UIBoard

class DLAlphaBetaSearchTests(unittest.TestCase):
    
    # def test_alpha_beta(self):
    #     fence_checker = FenceChecker(2, True)
    #     move_checker = MoveChecker()
    #     terminal_test = BoardTerminalTest()
        
    #     board = Board(
    #         fence_checker = fence_checker,
    #         move_checker = move_checker,
    #         grid_size = 5,
    #         player_positions = {
    #             Player.MAX : (2, 2),
    #             Player.MIN : (4, 4)
    #         },
    #         fences_horizontal = set(),
    #         fences_vertical = {(1, 3), (2, 3)}   
    #     )
    #     search = AlphaBetaSearch()

    #     strategy = search.find_strategy(board, terminal_test)
    #     best_action = strategy[board]
    #     self.assertTrue(isinstance(best_action, Move))
    #     self.assertEqual(strategy[board], Move((2, 2), (2, 3)))

    # def test_dl_alpha_beta(self):
    #     fence_checker = FenceChecker(2, True)
    #     move_checker = MoveChecker()
    #     terminal_test = BoardTerminalTest()

    #     board = Board(
    #         fence_checker = fence_checker,
    #         move_checker = move_checker,
    #         grid_size = 5,
    #         player_positions = {
    #             Player.MAX : (2, 2),
    #             Player.MIN : (4, 4)
    #         },
    #         fences_horizontal = set(),
    #         fences_vertical = {(1, 3), (2, 3)}
    #     )
    #     shortest_path_h = ShortestPathHeuristic()
    #     search = DLAlphaBetaSearch(depth = 3, heuristic = shortest_path_h)

    #     strategy = search.find_strategy(board, terminal_test)
    #     best_action = strategy[board]
    #     self.assertTrue(isinstance(best_action, Move))
    #     self.assertEqual(strategy[board], Move((2, 2), (2, 3)))

    def test_dl_alpha_beta_toggled(self):
        fence_checker = FenceChecker(2, True)
        move_checker = MoveChecker()
        terminal_test = BoardTerminalTest()

        board = Board(
            fence_checker = fence_checker,
            move_checker = move_checker,
            grid_size = 5,
            player_positions = {
                Player.MAX : (0, 0),
                Player.MIN : (2, 2)
            },
            current_player=Player.MIN,
            fences_horizontal = set(),
            fences_vertical = {(1, 0), (2, 0)}
        )
        board.toggle_player()
        shortest_path_h = ShortestPathHeuristic()
        search = DLAlphaBetaSearch(depth = 3, heuristic = shortest_path_h)

        strategy = search.find_strategy(board, terminal_test)
        best_action = strategy[board]
        print(best_action)
        UIBoard.print_board(board)
        UIBoard.print_board(board.get_action_result(best_action))
        self.assertTrue(isinstance(best_action, Move))
        self.assertEqual(strategy[board], Move((2, 2), (2, 1)))

    # def test_dl_alpha_beta_min_almost_wins(self):
    #     fence_checker = FenceChecker(2, True)
    #     move_checker = MoveChecker()
    #     terminal_test = BoardTerminalTest()

    #     board = Board(
    #         fence_checker = fence_checker,
    #         move_checker = move_checker,
    #         grid_size = 5,
    #         player_positions = {
    #             Player.MAX : (2, 2),
    #             Player.MIN : (3, 1)
    #         },
    #         fences_horizontal = set(),
    #         fences_vertical = set()
    #     )
    #     shortest_path_h = ShortestPathHeuristic()
    #     search = DLAlphaBetaSearch(depth = 5, heuristic = shortest_path_h)

    #     strategy = search.find_strategy(board, terminal_test)
    #     best_action = strategy[board]
    #     print(best_action)
    #     self.assertTrue(isinstance(best_action, PlaceFence))
    #     self.assertTrue(strategy[board] in [PlaceFence(True, (2, 0)), PlaceFence(True, (3, 0))])

    # def test_dl_alpha_beta_jump_over_opponent(self):
    #     fence_checker = FenceChecker(2, True)
    #     move_checker = MoveChecker()
    #     terminal_test = BoardTerminalTest()

    #     board = Board(
    #         fence_checker = fence_checker,
    #         move_checker = move_checker,
    #         grid_size = 5,
    #         player_positions = {
    #             Player.MAX : (2, 2),
    #             Player.MIN : (2, 3)
    #         },
    #         fences_horizontal = {(2, 3)},
    #         fences_vertical = {(1, 1), (2, 1)}
    #     )
    #     shortest_path_h = ShortestPathHeuristic()
    #     search = DLAlphaBetaSearch(depth = 5, heuristic = shortest_path_h)

    #     strategy = search.find_strategy(board, terminal_test)
    #     best_action = strategy[board]
    #     print(best_action)
    #     self.assertTrue(isinstance(best_action, Move))
    #     self.assertEqual(strategy[board], Move((2, 2), (1, 3)))

if __name__ == '__main__':
    unittest.main()
