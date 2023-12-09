import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import unittest
from Core.Player import Player
from GameFlow import FenceChecker, MoveChecker, Board

class TestBoardMethods(unittest.TestCase):
    def setUp(self):
        self.fence_checker = FenceChecker(fence_length=2, grid_size=9)
        self.grid_size = 9

    def test_identical_boards_equality(self):
        board1 = Board(self.fence_checker, MoveChecker(self.grid_size))
        board2 = Board(self.fence_checker, MoveChecker(self.grid_size))
        self.assertEqual(board1, board2)

    def test_different_boards_equality(self):
        board1 = Board(self.fence_checker, MoveChecker(self.grid_size))
        board2 = Board(self.fence_checker, MoveChecker(self.grid_size))
        board2.player_positions[Player.MAX] = (1, 1)  # Change position
        self.assertNotEqual(board1, board2)

    def test_hash_consistency_for_identical_boards(self):
        board1 = Board(self.fence_checker, MoveChecker(self.grid_size))
        board2 = Board(self.fence_checker, MoveChecker(self.grid_size))
        self.assertEqual(hash(board1), hash(board2))

    def test_hash_uniqueness_for_different_boards(self):
        board1 = Board(self.fence_checker, MoveChecker(self.grid_size))
        board2 = Board(self.fence_checker, MoveChecker(self.grid_size))
        board2.player_positions[Player.MAX] = (1, 1)  # Change position
        self.assertNotEqual(hash(board1), hash(board2))

    def test_equality_same_fence_configurations(self):
        fences = {(1, 2), (2, 3)}
        board1 = Board(self.fence_checker, MoveChecker(self.grid_size), fences_horizontal=fences)
        board2 = Board(self.fence_checker, MoveChecker(self.grid_size), fences_horizontal=fences)
        self.assertEqual(board1, board2)

    def test_inequality_different_horizontal_fences(self):
        board1 = Board(self.fence_checker, MoveChecker(self.grid_size), fences_horizontal={(1, 2)})
        board2 = Board(self.fence_checker, MoveChecker(self.grid_size), fences_horizontal={(2, 3)})
        self.assertNotEqual(board1, board2)

    def test_inequality_different_vertical_fences(self):
        board1 = Board(self.fence_checker, MoveChecker(self.grid_size), fences_vertical={(1, 2)})
        board2 = Board(self.fence_checker, MoveChecker(self.grid_size), fences_vertical={(2, 3)})
        self.assertNotEqual(board1, board2)

    def test_hash_different_fence_configurations(self):
        board1 = Board(self.fence_checker, MoveChecker(self.grid_size), fences_horizontal={(1, 2)})
        board2 = Board(self.fence_checker, MoveChecker(self.grid_size), fences_horizontal={(2, 3)})
        self.assertNotEqual(hash(board1), hash(board2))

if __name__ == '__main__':
    unittest.main()
