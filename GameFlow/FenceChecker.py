from Heuristics import ShortestPathHeuristic
from Actions import PlaceFence

class FenceChecker:
    """`FenceChecker` verifies validity and performs operations concerning fences"""
    def __init__(self, fence_length, should_check_for_obscured_path = False):
        self.fence_length = fence_length
        self.should_check_for_obscured_path = should_check_for_obscured_path
        self.shortest_path_h = ShortestPathHeuristic()

    def can_place_fence(self, board, coord, is_horizontal, fences_horizontal, fences_vertical) -> bool:
        """Returns true if fence can be placed at that cell; false otherwise"""
        # Check if the fence is within the bounds of the board
        if is_horizontal:
            if coord[0] > board.grid_size - self.fence_length or coord[1] >= board.grid_size:
                return False
        else:
            if coord[1] > board.grid_size - self.fence_length or coord[0] >= board.grid_size:
                return False

        # Check for overlapping fences
        if is_horizontal:
            for i in range(self.fence_length):
                if (coord[0] + i, coord[1]) in fences_horizontal:
                    return False
            # Check if it's connecting with another horizontal fence
            if ((coord[0] - 1, coord[1]) in fences_horizontal
                or (coord[0] + self.fence_length, coord[1]) in fences_horizontal):
                return False
        else:
            for i in range(self.fence_length):
                if (coord[0], coord[1] + i) in fences_vertical:
                    return False
            # Check if it's connecting with another vertical fence
            if ((coord[0], coord[1] - 1) in fences_vertical
                or (coord[0], coord[1] + self.fence_length) in fences_vertical):
                return False

        # Check if the new fence will not intersect with existing vertical fences
        if is_horizontal:
            for i in range(self.fence_length):
                if (coord[0] + i, coord[1]) in fences_vertical:
                    return False
        else:
            for i in range(self.fence_length):
                if (coord[0], coord[1] + i) in fences_horizontal:
                    return False

        # Check that the fence does not block all paths to the goal
        # This requires a pathfinding algorithm to ensure that both players still have
        # a path to win.
        # ...
        
        if not self.should_check_for_obscured_path:
            return True
        
        future_action = PlaceFence(is_horizontal, coord)
        future_board = board.get_action_result(future_action)
        
        if self.shortest_path_h(future_board) == float('inf'):
            return False
        else:
            return True

    def place_fence(self, board, coord, is_horizontal, fences_horizontal, fences_vertical):
        """Places the fence at the coordinate. If it's placed, return true; false otherwise"""
        if self.can_place_fence(board, coord, is_horizontal, fences_horizontal, fences_vertical):
            if is_horizontal:
                for i in range(self.fence_length):
                    fences_horizontal.add((coord[0] + i, coord[1]))
            else:
                for i in range(self.fence_length):
                    fences_vertical.add((coord[0], coord[1] + i))
            return True
        return False
