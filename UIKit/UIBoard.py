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

    def col_symb(in_cell, coord):
        same = (coord in self.fences_vertical)
        to_up = (up(coord) in self.fences_vertical)
        col_symb = " \u2016 " if (same or to_up) else " | "
        ret_val = in_cell + col_symb
        return ret_val

    def row_symb(coord):
        same = (coord in self.fences_horizontal)
        to_right = (left(coord) in self.fences_horizontal)
        row_symb = "===" if (same or to_right) else "---"
        return row_symb

    def in_cell_symb(coord):
        in_cell = self.player_position.get(coord)
        if in_cell is None:
            return " "
        else:
            return in_cell

    for i in range(0, self.board_size):
        row_line = ""
        col_line = "| "
        for j in range(0, self.board_size):
            coord_for_row = (j, i - 1)
            row_symb_for_coord = self.row_symb(coord_for_row)
            row_line += "-" + self.row_symb_for_coord
            
            in_cell = self.in_cell_symb((j, i))
            
            coord_for_col = (j, i)
            col_symb_for_coord = self.col_symb(in_cell, coord_for_col)
            col_line += col_symb_for_coord
            
        print(row_line)
        print(col_line)
        
    print("-" * board_size * 4)
