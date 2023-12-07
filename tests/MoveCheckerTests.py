import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import unittest
from Core import Player
from GameFlow import MoveChecker

class TestMoveChecker(unittest.TestCase):
    def setUp(self):
        self.board_size = 9
        self.move_checker = MoveChecker(self.board_size)

    def test_cant_jump_over_not_next_to_each_other(self):
        player_positions = {Player.MIN: (4, 0), Player.MAX: (4, 8)}

        self.assertEqual(
            self.move_checker.jump_over_coords(
                Player.MIN, Player.MAX,
                fences_horizontal = set(), fences_vertical = set(), 
                player_positions = player_positions
            ),
            set()
        )

    def test_is_within_board(self):
        self.assertTrue(self.move_checker.is_within_board((0, 0)))
        self.assertTrue(self.move_checker.is_within_board((8, 8)))
        self.assertFalse(self.move_checker.is_within_board((-1, 0)))
        self.assertFalse(self.move_checker.is_within_board((0, 9)))

    def test_is_fence_blocking(self):
        fences_horizontal = {(1, 1), (2, 3)}
        fences_vertical = {(4, 4), (5, 5)}

        self.assertTrue(
            self.move_checker.is_fence_blocking(
                (1, 1), (1, 2), fences_horizontal, fences_vertical
            )
        )

        self.assertTrue(
            self.move_checker.is_fence_blocking(
                (4, 5), (5, 5), fences_horizontal, fences_vertical
            )
        )

        self.assertFalse(
            self.move_checker.is_fence_blocking(
                (0, 0), (0, 1), fences_horizontal, fences_vertical
            )
        )
        self.assertFalse(
            self.move_checker.is_fence_blocking(
                (3, 2), (4, 2), fences_horizontal, fences_vertical
            )
        )

    def test_is_vertical_fence_blocking_horizontal_movement(self):
        fences_horizontal = {}
        fences_vertical = {(2, 1)}

        self.assertTrue(
            self.move_checker.is_fence_blocking(
                (2, 1), (3, 1), fences_horizontal, fences_vertical
            )
        )

        self.assertTrue(
            self.move_checker.is_fence_blocking(
                (2, 2), (3, 2), fences_horizontal, fences_vertical
            )
        )

    def test_can_jump_over_direct(self):
        player_positions = {Player.MIN: (2, 1), Player.MAX: (2, 2)}
        fences_horizontal = set()
        fences_vertical = set()

        self.assertEqual(
            self.move_checker.jump_over_coords(
                Player.MIN, Player.MAX, fences_horizontal, fences_vertical, player_positions
            ),
            set([(2, 3)])
        )

    def test_can_jump_over_to_sides(self):
        player_positions = {Player.MIN: (2, 1), Player.MAX: (2, 2)}
        fences_horizontal = {(2, 2)}
        fences_vertical = set()

        self.assertEqual(
            self.move_checker.jump_over_coords(
                Player.MIN, Player.MAX, fences_horizontal, fences_vertical, player_positions
            ),
            set([(1, 2), (3, 2)])
        )

    def test_can_jump_over_to_one_side(self):
        player_positions = {Player.MIN: (2, 1), Player.MAX: (2, 2)}
        fences_horizontal = {(2, 2)}
        fences_vertical = {(2, 1)}

        self.assertEqual(
            self.move_checker.jump_over_coords(
                Player.MIN, Player.MAX,
                fences_horizontal, fences_vertical, 
                player_positions = player_positions
            ),
            set([(1, 2)])
        )

# Add more tests as needed to cover all scenarios

if __name__ == '__main__':
    unittest.main()
