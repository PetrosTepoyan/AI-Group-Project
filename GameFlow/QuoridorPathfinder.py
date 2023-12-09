from collections import deque
from Core import Player
from GameFlow.MoveChecker import left, up

class QuoridorPathfinder:
    """Class for """
    def __init__(self, fences_horizontal, fences_vertical, grid_size):
        self.fences_horizontal = fences_horizontal
        self.fences_vertical = fences_vertical
        self.grid_size = grid_size

    def is_path_blocked(self, from_coord, to_coord, is_horizontal) -> bool:
        """Returns true if path between two adjacent cells is blocked`by a type of fence"""
        if is_horizontal:
            return ((from_coord, to_coord) in self.fences_horizontal
                    or up(from_coord) in self.fences_horizontal)
        return ((from_coord, to_coord) in self.fences_vertical
                or left(from_coord) in self.fences_vertical)

    def get_neighbors(self, position) -> list[tuple[int, int]]:
        """Returns a list of accessible neighboring cells"""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Down, Right, Up, Left
        neighbors = []
        for d in directions:
            neighbor = (position[0] + d[0], position[1] + d[1])
            if (0 <= neighbor[0] < self.grid_size and 0 <= neighbor[1] < self.grid_size
                and not self.is_path_blocked(position, neighbor, d[1] == 0)):
                neighbors.append(neighbor)
        return neighbors

    def bfs(self, start, goal_line) -> bool:
        """Breadth-First Search implementation"""
        queue = deque([start])
        visited = set([start])

        while queue:
            current = queue.popleft()
            if current[1] == goal_line:
                return True  # Reached the goal line

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return False  # No path found

    def path_exists_for_both_players(self, player_positions):
        """Returns true if a path exists for both players; false otherwise"""
        # Player.MAX tries to reach the bottom row (grid_size - 1),
        # and Player.MIN tries to reach the top row (0)
        return (self.bfs(player_positions[Player.MAX], self.grid_size - 1)
                and self.bfs(player_positions[Player.MIN], 0))
