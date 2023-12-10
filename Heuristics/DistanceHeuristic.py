from GameFlow import Board
from Core import Player

class DistanceHeuristic:
    """Simple distance heuristic"""
    # Atmost distance + min(num of fences on the way, 1)
    def __call__(self, board: Board, position=None):
        player = board.current_player
        if position is None:
            position = board.player_positions[player]
            
        if player == Player.MAX:
            distance = board.grid_size - position[1] - 1
            return distance
        else:
            distance = position[1] - 1
            return distance
