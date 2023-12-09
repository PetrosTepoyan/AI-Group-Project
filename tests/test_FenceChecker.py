import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from GameFlow import FenceChecker
import unittest

class FenceCheckerTests(unittest.TestCase):
    def setUp(self):
        # Setup a 9x9 board with a default fence length of 2 for these tests
        self.checker = FenceChecker(grid_size=9, fence_length=2)

    def test_fence_within_bounds_horizontal(self):
        # Test that a horizontal fence within bounds can be placed
        self.assertTrue(self.checker.can_place_fence((0, 0), True, set(), set()))

    def test_fence_within_bounds_vertical(self):
        # Test that a vertical fence within bounds can be placed
        self.assertTrue(self.checker.can_place_fence((0, 0), False, set(), set()))

    def test_fence_out_of_bounds_horizontal(self):
        # Test that a horizontal fence out of bounds cannot be placed
        self.assertFalse(self.checker.can_place_fence((8, 0), True, set(), set()))

    def test_fence_out_of_bounds_vertical(self):
        # Test that a vertical fence out of bounds cannot be placed
        self.assertFalse(self.checker.can_place_fence((0, 8), False, set(), set()))

    def test_fence_overlap_horizontal(self):
        # Test that an overlapping horizontal fence cannot be placed
        fences_horizontal = {(1, 1)}
        self.assertFalse(self.checker.can_place_fence((1, 1), True, fences_horizontal, set()))

    def test_fence_overlap_vertical(self):
        # Test that an overlapping vertical fence cannot be placed
        fences_vertical = {(1, 1)}
        self.assertFalse(self.checker.can_place_fence((1, 1), False, set(), fences_vertical))

    def test_connecting_fence_horizontal(self):
        # Test that a horizontal fence connecting to another cannot be placed
        fences_horizontal = {(2, 1)}
        self.assertFalse(self.checker.can_place_fence((1, 1), True, fences_horizontal, set()))

    def test_connecting_fence_vertical(self):
        # Test that a vertical fence connecting to another cannot be placed
        fences_vertical = {(1, 2)}
        self.assertFalse(self.checker.can_place_fence((1, 1), False, set(), fences_vertical))

    def test_fence_same_place(self):
        fences_horizontal = {(0, 0)}
        self.assertFalse(self.checker.can_place_fence((0,0), True, fences_horizontal, set()))

    # More tests should be written to check intersections and path blocking

if __name__ == '__main__':
    unittest.main()
