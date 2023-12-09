import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import unittest
from Core import Player
from GameFlow import Board, FenceChecker, MoveChecker

class TestMoveChecker(unittest.TestCase):

    def setUp(self):
        self.board_size = 9
        self.move_checker = MoveChecker(self.board_size)
        self.board = Board(FenceChecker(grid_size=self.board_size, fence_length=2), self.move_checker)

    def test_cant_jump_over_not_next_to_each_other(self):
        player_coord = (4, 0)
        opponent_coord = (4, 8)

        self.assertEqual(
            self.move_checker.jump_over_coords(player_coord, opponent_coord),
            set()
        )

    def test_is_within_board(self):
        self.assertTrue(self.move_checker.is_within_board((0, 0)))
        self.assertTrue(self.move_checker.is_within_board((8, 8)))
        self.assertFalse(self.move_checker.is_within_board((-1, 0)))
        self.assertFalse(self.move_checker.is_within_board((0, 9)))

    def test_is_fence_blocking(self):
        self.board.fences_horizontal = {(1, 1), (2, 3)}
        self.board.fences_vertical = {(4, 4), (5, 5)}

        self.assertTrue(
            self.move_checker.is_fence_blocking((1, 1), (1, 2))
        )

        self.assertTrue(
            self.move_checker.is_fence_blocking(
                (4, 5), (5, 5)
            )
        )

        self.assertFalse(
            self.move_checker.is_fence_blocking(
                (0, 0), (0, 1)
            )
        )
        self.assertFalse(
            self.move_checker.is_fence_blocking(
                (3, 2), (4, 2)
            )
        )

    def test_is_vertical_fence_blocking_horizontal_movement(self):
        self.board.fences_horizontal = {}
        self.board.fences_vertical = {(2, 1)}

        # From Left to right
        self.assertTrue(
            self.move_checker.is_fence_blocking(
                (2, 1), (3, 1)
            )
        )

        self.assertTrue(
            self.move_checker.is_fence_blocking(
                (2, 2), (3, 2)
            )
        )

        # From right to left
        self.assertTrue(
            self.move_checker.is_fence_blocking(
                (3, 1), (2, 1)
            )
        )

        self.assertTrue(
            self.move_checker.is_fence_blocking(
                (3, 2), (2, 2)
            )
        )

        # FALSE
        self.assertFalse(
            self.move_checker.is_fence_blocking(
                (2, 1), (1, 1)
            )
        )

        self.assertFalse(
            self.move_checker.is_fence_blocking(
                (2, 2), (1, 2)
            )
        )

    def test_is_horizontal_fence_blocking_vertical_movement(self):
        self.board.fences_horizontal = {(2, 1)}
        self.board.fences_vertical = {}

        self.assertTrue(
            self.move_checker.is_fence_blocking(
                (2, 1), (2, 2)
            )
        )

        self.assertTrue(
            self.move_checker.is_fence_blocking(
                (3, 1), (3, 2)
            )
        )

    def test_can_jump_over_direct(self):
        player_coord = (2, 1)
        opponent_coord = (2, 2)
        self.board.fences_horizontal = set()
        self.board.fences_vertical = set()

        self.assertEqual(
            self.move_checker.jump_over_coords(
                player_coord, opponent_coord
            ),
            set([(2, 3)])
        )

    def test_can_jump_over_to_sides(self):
        player_coord = (2, 1)
        opponent_coord = (2, 2)
        self.board.fences_horizontal = {(2, 2)}
        self.board.fences_vertical = set()

        self.assertEqual(
            self.move_checker.jump_over_coords(
                player_coord, opponent_coord
            ),
            set([(1, 2), (3, 2)])
        )

    def test_can_jump_over_to_one_side(self):
        player_coord = (2, 1)
        opponent_coord = (2, 2)
        self.board.fences_horizontal = {(2, 2)}
        self.board.fences_vertical = {(2, 1)}

        self.assertEqual(
            self.move_checker.jump_over_coords(
                player_coord, opponent_coord
            ),
            set([(1, 2)])
        )

# Add more tests as needed to cover all scenarios

if __name__ == '__main__':
    unittest.main()
