from Core import Player
from collections import deque

class QuoridorPathfinder:
    def __init__(self, fences_horizontal, fences_vertical, grid_size):
        self.fences_horizontal = fences_horizontal
        self.fences_vertical = fences_vertical
        self.grid_size = grid_size

    def is_path_blocked(self, from_coord, to_coord, is_horizontal):
        if is_horizontal:
            return (from_coord, to_coord) in self.fences_horizontal or (from_coord[0], from_coord[1] - 1) in self.fences_horizontal
        else:
            return (from_coord, to_coord) in self.fences_vertical or (from_coord[0] - 1, from_coord[1]) in self.fences_vertical

    def get_neighbors(self, position):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Down, Right, Up, Left
        neighbors = []
        for d in directions:
            neighbor = (position[0] + d[0], position[1] + d[1])
            if 0 <= neighbor[0] < self.grid_size and 0 <= neighbor[1] < self.grid_size and not self.is_path_blocked(position, neighbor, d[1] == 0):
                neighbors.append(neighbor)
        return neighbors

    def bfs(self, start, goal_line):
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
        # Player.MAX tries to reach the bottom row (grid_size - 1), and Player.MIN tries to reach the top row (0)
        return self.bfs(player_positions[Player.MAX], self.grid_size - 1) and self.bfs(player_positions[Player.MIN], 0)
