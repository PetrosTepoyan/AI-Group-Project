import heapq
from copy import deepcopy
from Core import Player
from GameFlow import Board
from Heuristics import DistanceHeuristic

class ShortestPathHeuristic:

    def __init__(self):
        self.distance_heuristic = DistanceHeuristic()

    def __call__(self, board: Board, print_path: bool = False):
        """Shortest-path heuristic """
        board_copy = deepcopy(board)
        player = board_copy.current_player
        target_line = board_copy.grid_size - 1 if player == Player.MAX else 0
        return (self.a_star(board_copy, board_copy.player_positions[player], target_line, print_path)
                + self.distance_heuristic(board, board_copy.player_positions[board_copy.current_opponent]))

    def recover_path(self, came_from: dict, current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path = [current] + total_path
        return total_path

    def a_star(self, board: Board, start, target_line, print_path: bool = False):
        """Classic A*-search"""
        # Define the priority queue
        open_set = []
        heapq.heappush(open_set, (0, start))

        # Map for path recovery
        came_from = dict()

        # Costs from start to a node
        g_score = {start: 0}
        while open_set:
            current = heapq.heappop(open_set)[1]

            # Check if reached the target line
            if current[1] == target_line:
                if print_path:
                    print(self.recover_path(came_from, current))
                return g_score[current]

            for neighbor in self.get_neighbors(board, current):
                # print(f"visited neighbor {neighbor}")
                tentative_g_score = g_score[current] + 1  # Assume cost=1 for each move
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    if print_path:
                        came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(board, neighbor)
                    # print(f"added neighbor {neighbor} with f_score {f_score}")
                    heapq.heappush(open_set, (f_score, neighbor))

        return float('inf')  # Return a high cost if no path found

    def get_neighbors(self, board: Board, node):
        """Get the neighboring nodes in the board"""
        return board.move_checker.get_movable_coords(
            board,
            player_coord=node
        )

    def heuristic(self, board: Board, node):
        """Get primitive heuristic for A*-search"""
        return self.distance_heuristic(board, node)
