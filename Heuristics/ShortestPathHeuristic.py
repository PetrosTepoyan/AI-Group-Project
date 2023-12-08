from GameFlow import Board
from Core import Player
import heapq

class ShortestPathHeuristic:
    def __call__(self, board: Board):
        player = board.current_player
        target_line = board.grid_size - 1 if player == Player.MAX else 0
        return self.a_star(board, player.position, target_line)

    def a_star(self, board, start, target_line):
        # Define the priority queue
        open_set = []
        heapq.heappush(open_set, (0, start))

        # Costs from start to a node
        g_score = {start: 0}

        while open_set:
            current = heapq.heappop(open_set)[1]

            # Check if reached the target line
            if (player == Player.MAX and current[1] == target_line) or \
               (player == Player.MIN and current[1] == target_line):
                return g_score[current]

            for neighbor in self.get_neighbors(board, current):
                tentative_g_score = g_score[current] + 1  # Assume cost=1 for each move
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, target_line)
                    heapq.heappush(open_set, (f_score, neighbor))

        return float('inf')  # Return a high cost if no path found

    def get_neighbors(self, board, node):
        board

    def heuristic(self, node: Board, target_line):
        
