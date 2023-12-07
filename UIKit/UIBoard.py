from Core import Player

class UIBoard:
    def __init__(self, board_size = 9, fences_horizontal = set(), fences_vertical = set(), player_positions = {
            Player.MAX: (4, 0),
            Player.MIN: (4, 8),
        }):
        self.board_size = board_size
        self.fences_horizontal = fences_horizontal
        self.fences_vertical = fences_vertical
        self.player_positions = player_positions

    def draw(self):
        tile_size = 3
        row = "--" * (self.board_size * 2) + "-"
        cell = "| X " * self.board_size + "|"
        for _ in range(self.board_size):
            print(row)
            print(cell)
        print(row)

