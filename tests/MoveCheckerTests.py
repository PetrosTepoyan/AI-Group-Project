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

# Add more tests as needed to cover all scenarios

if __name__ == '__main__':
    unittest.main()
