
class FenceChecker:
    def __init__(self, grid_size, fence_length):
        self.grid_size = grid_size
        self.fence_length = fence_length

    def can_place_fence(self, coord, is_horizontal, fences_horizontal, fences_vertical):
        # Check if the fence is within the bounds of the board
        if is_horizontal:
            if coord[0] > self.grid_size - self.fence_length or coord[1] >= self.grid_size:
                return False
        else:
            if coord[1] > self.grid_size - self.fence_length or coord[0] >= self.grid_size:
                return False

        # Check for overlapping fences
        if is_horizontal:
            for i in range(self.fence_length):
                if (coord[0] + i, coord[1]) in fences_horizontal:
                    return False
            # Check if it's connecting with another horizontal fence
            if (coord[0] - 1, coord[1]) in fences_horizontal or (coord[0] + self.fence_length, coord[1]) in fences_horizontal:
                return False
        else:
            for i in range(self.fence_length):
                if (coord[0], coord[1] + i) in fences_vertical:
                    return False
            # Check if it's connecting with another vertical fence
            if (coord[0], coord[1] - 1) in fences_vertical or (coord[0], coord[1] + self.fence_length) in fences_vertical:
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
        # This requires a pathfinding algorithm to ensure that both players still have a path to win.
        # ...

        return True

    def place_fence(self, coord, is_horizontal, fences_horizontal, fences_vertical):
        if self.can_place_fence(coord, is_horizontal):
            if is_horizontal:
                for i in range(self.fence_length):
                    fences_horizontal.add((coord[0] + i, coord[1]))
            else:
                for i in range(self.fence_length):
                    fences_vertical.add((coord[0], coord[1] + i))
            return True
        else:
            return False
