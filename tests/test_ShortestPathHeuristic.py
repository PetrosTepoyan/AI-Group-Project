import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from Core import Player
from GameFlow import Board, FenceChecker, MoveChecker
from Heuristics.ShortestPathHeuristic import ShortestPathHeuristic

import unittest

class TestShortestPathHeuristic(unittest.TestCase):

    def setUp(self):
        self.board_size = 5
        self.board = Board(FenceChecker(grid_size=self.board_size, fence_length=2), MoveChecker())

    def test_no_fences(self):
        self.assertEqual(ShortestPathHeuristic()(board=self.board), 4)

    def test_avoid_one_fence(self):
        self.board.fences_horizontal = {(1, 0)}
        self.board.fences_vertical = {}

        self.assertEqual(ShortestPathHeuristic()(board=self.board,), 5)

    def test_avoid_long_fence(self):
        self.board.fences_horizontal = {(1, 0), (3, 0)}

        self.assertEqual(ShortestPathHeuristic()(board=self.board, print_path=True), 6)

    def test_dead_end(self):
        self.board.fences_horizontal = {(1, 0)}
        self.board.fences_vertical = {(0, 0), (2, 0)}

        self.assertEqual(ShortestPathHeuristic()(board=self.board), float('inf'))
    
    def test_corridor_with_opponent(self):
        self.board.fences_vertical = {(1, 1), (2, 1), (1, 3), (2, 3)}
        self.board.player_positions[Player.MIN] = (2, 2)

        self.assertEqual(ShortestPathHeuristic()(board=self.board), 3)
    
    def test_diagonal_jump_over_opponent(self):
        self.board.fences_vertical = {(1, 1), (2, 1)}
        self.board.fences_horizontal = {(1, 3), (3, 3)}
        self.board.player_positions[Player.MIN] = (2, 3)

        self.assertEqual(ShortestPathHeuristic()(board=self.board), 5)
    
    def test_snake_maze(self):
        self.board.fences_horizontal = {(0, 0), (2, 0), (1, 1), (3, 1), (0, 2), (2, 2), (1, 3), (3, 3)}
        self.board.player_positions[Player.MAX] = (0, 0)

        self.assertEqual(ShortestPathHeuristic()(board=self.board), 20)

if __name__ == '__main__':
    unittest.main()
