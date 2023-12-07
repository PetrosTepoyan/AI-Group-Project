from GameFlow import Board
from Core import Player

class DistanceHeuristic:
    def __call__(self, board: Board):
        player = board.current_player
        position = board.player_positions[player]
        if player == Player.MAX:
            distance = board.grid_size - position[1]
        else:
            distance = position[1]
        return distance