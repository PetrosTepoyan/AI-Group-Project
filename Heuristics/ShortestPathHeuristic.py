import heapq
from Core import Player
from GameFlow import Board
from Heuristics import DistanceHeuristic

class ShortestPathHeuristic:
    """Shortest-path heuristic """
    def __call__(self, board: Board):
        player = board.current_player
        target_line = board.grid_size - 1 if player == Player.MAX else 0
        return self.a_star(board, player.position, target_line)

    def a_star(self, board: Board, start, target_line):
        """Classic A*-search"""
        # Define the priority queue
        open_set = []
        heapq.heappush(open_set, (0, start))

        # Costs from start to a node
        g_score = {start: 0}

        while open_set:
            current = heapq.heappop(open_set)[1]

            # Check if reached the target line
            if current[1] == target_line:
                return g_score[current]

            for neighbor in self.get_neighbors(board, current):
                tentative_g_score = g_score[current] + 1  # Assume cost=1 for each move
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(board, neighbor)
                    heapq.heappush(open_set, (f_score, neighbor))

        return float('inf')  # Return a high cost if no path found

    def get_neighbors(self, board: Board, node):
        """Get the neighboring nodes in the board"""
        return board.move_checker.get_movable_coords(player_coord=node)

    def heuristic(self, board: Board, node):
        """Get primitive heuristic for A*-search"""
        return DistanceHeuristic(board, node)
