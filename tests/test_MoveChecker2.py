import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import unittest
from Core import Player
from GameFlow import Board, FenceChecker, MoveChecker

class TestMoveChecker(unittest.TestCase):

    def setUp(self):
        self.board_size = 9
        self.move_checker = MoveChecker()
        self.board = Board(FenceChecker(self.board_size, 2), self.move_checker)

    def test_movable_coords_at_top(self):
        player_coord = (4, 0)
        opponent_coord = (4, 8)
        self.assertEqual(
            self.move_checker.get_movable_coords(
                self.board,
                player_coord, opponent_coord
            ),
            {(3, 0), (5, 0), (4, 1)}
        )

    def test_movable_coords_at_right_corner(self):
        player_coord = (8, 0)
        opponent_coord = (4, 8)
        self.assertEqual(
            self.move_checker.get_movable_coords(
                self.board, 
                player_coord, opponent_coord
            ),
            {(7, 0), (8, 1)}
        )

    def test_movable_coords_at_center(self):
        player_coord = (4, 1)
        opponent_coord = (4, 8)
        self.assertEqual(
            self.move_checker.get_movable_coords(
                self.board,
                player_coord, opponent_coord
            ),
            {(4, 0), (4, 2), (3, 1), (5, 1)}
        )


    def test_move_through_fence(self):
        self.board.fences_horizontal = {(0, 0)}
        self.board.fences_vertical = {}

        self.assertTrue(
            self.move_checker.is_fence_blocking(
                self.board,
                (1, 1), (1, 0)
            )
        )


# Add more tests as needed to cover all scenarios

if __name__ == '__main__':
    unittest.main()
