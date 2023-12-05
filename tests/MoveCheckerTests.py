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
        self.assertTrue(
            self.move_checker.is_fence_blocking(
                (4, 0), (4, 1),
                self.fences_horizontal, 
                self.fences_vertical
            )
        )
        self.assertFalse(
            self.move_checker.is_fence_blocking(
                (3, 0), (3, 1), 
                self.fences_horizontal, 
                self.fences_vertical
            )
        )
        
        self.fences_vertical.add((1, 0))
        self.assertTrue(
            self.move_checker.is_fence_blocking(
                (1, 0), (2, 0),
                self.fences_horizontal, 
                self.fences_vertical
            )
        )
        self.assertFalse(
            self.move_checker.is_fence_blocking(
                (1, 0), (1, 1), 
                self.fences_horizontal, 
                self.fences_vertical
            )
        )

    def test_can_move_no_fence(self):
        self.assertFalse(
            self.move_checker.can_move(
                Player.MAX, (4, -1), # up
                self.fences_horizontal, 
                self.fences_vertical,
                self.player_positions
            )
        )
        
        self.assertTrue(
            self.move_checker.can_move(
                Player.MAX, (4, 1), # down
                self.fences_horizontal, 
                self.fences_vertical,
                self.player_positions
            )
        )
        
        self.assertTrue(
            self.move_checker.can_move(
                Player.MAX, (3, 0), # left
                self.fences_horizontal, 
                self.fences_vertical,
                self.player_positions
            )
        )
        
        self.assertTrue(
            self.move_checker.can_move(
                Player.MIN, (4, 7), # up 
                self.fences_horizontal, 
                self.fences_vertical,
                self.player_positions
            )
        )
        
        self.assertTrue(
            self.move_checker.can_move(
                Player.MIN, (5, 8), # right 
                self.fences_horizontal, 
                self.fences_vertical,
                self.player_positions
            )
        )

    def test_can_move_with_fence(self):
        self.fences_vertical.add((4, 0))
        self.assertTrue(
            self.move_checker.can_move(
                Player.MAX,
                (4, 1),
                self.fences_horizontal,
                self.fences_vertical,
                self.player_positions
            )
        )

    def test_can_jump_over_opponent(self):
        self.player_positions[Player.MIN] = (4, 1)
        self.assertTrue(
            self.move_checker.can_jump_over(
                Player.MAX, Player.MIN, 
                self.fences_horizontal, 
                self.fences_vertical,
                self.player_positions
            )
        )
        
    def test_can_not_jump_over_opponent_because_of_board_size(self):
        self.player_positions[Player.MIN] = (4, 1)
        self.assertFalse(
            self.move_checker.can_jump_over(
                Player.MIN, Player.MAX, 
                self.fences_horizontal, 
                self.fences_vertical,
                self.player_positions
            )
        )

    def test_can_not_jump_over_opponent_with_fence(self):
        self.player_positions[Player.MIN] = (4, 1)
        self.fences_horizontal.add((4, 1))
        self.assertFalse(
            self.move_checker.can_jump_over(
                Player.MAX,
                Player.MIN,
                self.fences_horizontal,
                self.fences_vertical, 
                self.player_positions
            )
        )

    def test_can_jump_over_opponent_diagonally(self):
        self.player_positions[Player.MIN] = (4, 1)
        self.fences_horizontal.add((4, 1))
        self.assertTrue(
            self.move_checker.can_jump_over(
                Player.MAX, Player.MIN, 
                self.fences_horizontal,
                self.fences_vertical, 
                self.player_positions
            )
        )
        
    def test_move_in_all_directions(self):
        self.player_positions = {Player.MIN: (4, 1), Player.MAX: (4, 8)}
        expected_moves = set([(4, 0), (3, 1), (5, 1), (4, 2)])
        movable_coords = self.move_checker.get_movable_coords_G(
            player=Player.MIN,
            opponent=Player.MAX,
            fences_horizontal=self.fences_horizontal,
            fences_vertical=self.fences_vertical,
            player_positions=self.player_positions
        )
        self.assertEqual(movable_coords, expected_moves)
        
    def test_move_blocked_by_fence_on_same_level(self):
        
        self.fences_vertical.add((4, 0))
        
        self.player_positions = {Player.MIN: (4, 1), Player.MAX: (4, 8)}
        expected_moves = set([(4, 0), (3, 1), (4, 2)])
        movable_coords = self.move_checker.get_movable_coords_G(
            player=Player.MIN,
            opponent=Player.MAX,
            fences_horizontal=self.fences_horizontal,
            fences_vertical=self.fences_vertical,
            player_positions=self.player_positions
        )
        self.assertEqual(movable_coords, expected_moves)
        
    def test_move_blocked_by_fence_on_same_level_and_player_at_edge(self):
        
        self.fences_vertical.add((4, 0))
        
        self.player_positions = {Player.MIN: (4, 0), Player.MAX: (4, 8)}
        expected_moves = set([(3, 0), (4, 1)])
        movable_coords = self.move_checker.get_movable_coords_G(
            player=Player.MIN,
            opponent=Player.MAX,
            fences_horizontal=self.fences_horizontal,
            fences_vertical=self.fences_vertical,
            player_positions=self.player_positions
        )
        self.assertEqual(movable_coords, expected_moves)

    def test_jump_over_opponent(self):
        self.player_positions = {Player.MIN: (4, 4), Player.MAX: (4, 5)}
        self.player_positions[Player.MAX] = (4, 4)
        
        expected_moves = set([(4, 3), (4, 5), (4, 6)])  # Jump over the opponent
        movable_coords = self.move_checker.get_movable_coords_G(
            player=Player.MIN,
            opponent=Player.MAX,
            fences_horizontal=self.fences_horizontal,
            fences_vertical=self.fences_vertical,
            player_positions=self.player_positions
        )
        self.assertEqual(movable_coords, expected_moves)

    def test_diagonal_jump_due_to_fence(self):
        self.player_positions = {Player.MIN: (4, 4), Player.MAX: (4, 5)}
        self.player_positions[Player.MAX] = (4, 4)
        
        self.fences_horizontal.add((4, 4))
        expected_moves = set([(4, 3), (3, 5), (5, 5)])  # Diagonal jumps
        movable_coords = self.move_checker.get_movable_coords_G(
            player=Player.MIN,
            opponent=Player.MAX,
            fences_horizontal=self.fences_horizontal,
            fences_vertical=self.fences_vertical,
            player_positions=self.player_positions
        )
        self.assertEqual(movable_coords, expected_moves)

    def test_move_at_board_edge(self):
        self.player_positions = {Player.MIN: (0, 4), Player.MAX: (4, 5)} # Player at the top edge
        
        expected_moves = set([(1, 4), (0, 3), (0, 5)])
        movable_coords = self.move_checker.get_movable_coords_G(
            player=Player.MIN,
            opponent=Player.MAX,
            fences_horizontal=self.fences_horizontal,
            fences_vertical=self.fences_vertical,
            player_positions=self.player_positions
        )
        self.assertEqual(movable_coords, expected_moves)

    def test_lateral_movement_around_opponent(self):
        self.player_positions = {Player.MIN: (4, 4), Player.MAX: (4, 5)}
        self.player_positions[Player.MAX] = (4, 5)
        
        self.fences_vertical.add((4, 5))
        expected_moves = set([(3, 4), (4, 3), (4, 6)])  # Move around the opponent laterally
        movable_coords = self.move_checker.get_movable_coords_G(
            player=Player.MIN,
            opponent=Player.MAX,
            fences_horizontal=self.fences_horizontal,
            fences_vertical=self.fences_vertical,
            player_positions=self.player_positions
        )
        self.assertEqual(movable_coords, expected_moves)

if __name__ == '__main__':
    unittest.main()
