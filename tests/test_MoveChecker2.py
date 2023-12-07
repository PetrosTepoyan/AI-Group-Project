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
        
    def test_movable_coords_at_top(self):
        player_positions = {Player.MIN: (4, 0), Player.MAX: (4, 8)}
        self.assertEqual(
            self.move_checker.get_movable_coords(
                Player.MIN, Player.MAX,
                fences_horizontal = set(), fences_vertical = set(), 
                player_positions = player_positions
            ),
            {(3, 0), (5, 0), (4, 1)}
        )
        
    def test_movable_coords_at_right_corner(self):
        player_positions = {Player.MIN: (8, 0), Player.MAX: (4, 8)}
        self.assertEqual(
            self.move_checker.get_movable_coords(
                Player.MIN, Player.MAX,
                fences_horizontal = set(), fences_vertical = set(), 
                player_positions = player_positions
            ),
            {(7, 0), (8, 1)}
        )
        
    def test_movable_coords_at_center(self):
        player_positions = {Player.MIN: (4, 1), Player.MAX: (4, 8)}
        self.assertEqual(
            self.move_checker.get_movable_coords(
                Player.MIN, Player.MAX,
                fences_horizontal = set(), fences_vertical = set(), 
                player_positions = player_positions
            ),
            {(4, 0), (4, 2), (3, 1), (5, 1)}
        )
        
        
    def test_move_through_fence(self):
        fences_horizontal = {(0, 0)}
        fences_vertical = {}

        self.assertTrue(
            self.move_checker.is_fence_blocking(
                (1, 1), (1, 0), fences_horizontal, fences_vertical
            )
        )
        

# Add more tests as needed to cover all scenarios

if __name__ == '__main__':
    unittest.main()
