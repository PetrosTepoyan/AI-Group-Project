from GameFlow import Board
from Core import Player

class DistanceHeuristic:
    def __call__(self, board: Board):
        player = board.current_player
        position = board.player_positions[player]
        if player == Player.MAX:
            distance = board.grid_size - position[1]
            
            for fence in board.fences_horizontal:
                b1 = fence[0] == position[0]
                b2 = fence[0] == (position[0] - 1)
                b3 = fence[0] == (position[0] + 1)
                b4 = fence[1] >= position[1]
                if (b1 or b2 or b3) and b4:
                    distance -= 1
            
        else:
            distance = position[1]
            
            for fence in board.fences_horizontal:
                b1 = fence[0] == position[0]
                b2 = fence[0] == (position[0] - 1)
                b3 = fence[0] == (position[0] + 1)
                b4 = fence[1] <= position[1]
                if (b1 or b2 or b3) and b4:
                    distance -= 1
            
        return distance