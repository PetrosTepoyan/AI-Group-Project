import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import unittest
from Core import Player
from GameFlow import MoveChecker

class TestMoveChecker(unittest.TestCase):
    def setUp(self):
        self.board_size = 9
        self.fences_horizontal = set()
        self.fences_vertical = set()
        self.player_positions = {
            Player.MAX: (4, 0),
            Player.MIN: (4, 8),
        }
        self.move_checker = MoveChecker(self.board_size)

    def test_within_board(self):
        self.assertTrue(self.move_checker.is_within_board((0, 0)))
        self.assertTrue(self.move_checker.is_within_board((8, 8)))
        self.assertFalse(self.move_checker.is_within_board((-1, 0)))
        self.assertFalse(self.move_checker.is_within_board((0, 9)))

    def test_is_fence_blocking(self):
        self.fences_horizontal.add((4, 0))
        self.assertTrue(self.move_checker.is_fence_blocking((4, 0), (4, 1), self.fences_horizontal, self.fences_vertical))
        self.assertFalse(self.move_checker.is_fence_blocking((3, 0), (3, 1), self.fences_horizontal, self.fences_vertical))

    def test_can_move_no_fence(self):
        self.assertTrue(self.move_checker.can_move(Player.MAX, (4, 1), self.fences_horizontal, self.fences_vertical, self.player_positions))

    def test_can_move_with_fence(self):
        self.fences_vertical.add((4, 0))
        self.assertFalse(self.move_checker.can_move(Player.MAX, (4, 1), self.fences_horizontal, self.fences_vertical, self.player_positions))

    def test_can_jump_over_opponent(self):
        self.player_positions[Player.MIN] = (4, 1)
        self.assertTrue(self.move_checker.can_jump_over(Player.MAX, Player.MIN, self.fences_horizontal, self.fences_vertical, self.player_positions))

    def test_can_not_jump_over_opponent_with_fence(self):
        self.player_positions[Player.MIN] = (4, 1)
        self.fences_horizontal.add((4, 1))
        self.assertFalse(self.move_checker.can_jump_over(Player.MAX, Player.MIN, self.fences_horizontal, self.fences_vertical, self.player_positions))

    def test_can_jump_over_opponent_diagonally(self):
        self.player_positions[Player.MIN] = (4, 1)
        self.fences_horizontal.add((4, 1))
        self.assertTrue(self.move_checker.can_jump_over(Player.MAX, Player.MIN, self.fences_horizontal, self.fences_vertical, self.player_positions))


if __name__ == '__main__':
    unittest.main()
