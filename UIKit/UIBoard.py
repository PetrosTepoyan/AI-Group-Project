from Core import Player

class UIBoard:
    def __init__(self, board_size = 9, fences_horizontal = set(), fences_vertical = set(), player_positions = {
            Player.MAX: (4, 0),
            Player.MIN: (4, 8),
        }):
        self.board_size = board_size
        self.fences_horizontal = fences_horizontal
        self.fences_vertical = fences_vertical
        self.player_positions = { value : ("X" if key == Player.MAX else "O") for key, value in player_positions.items()}

    def col_symb(self, in_cell, coord):
        same = (coord in self.fences_vertical)
        to_up = (up(coord) in self.fences_vertical)
        col_symb = " \u2016 " if (same or to_up) else " | "
        ret_val = in_cell + col_symb
        return ret_val

    def row_symb(self, coord):
        same = (coord in self.fences_horizontal)
        to_right = (left(coord) in self.fences_horizontal)
        row_symb = "===" if (same or to_right) else "---"
        return row_symb

    def in_cell_symb(self, coord):
        in_cell = self.player_positions.get(coord)
        if in_cell is None:
            return " "
        else:
            return in_cell

    def print(self):
        print("    " + "   ".join([str(i) for i in range(self.board_size)]))
        for i in range(0, self.board_size):
            row_line = "  "
            col_line = str(i) + " | "
            for j in range(0, self.board_size):
                coord_for_row = (j, i - 1)
                if i == 0:
                    row_line = "  " + "-" * (self.board_size * 4 + 1)
                else:
                    row_symb_for_coord = self.row_symb(coord_for_row)
                    row_line += "-" + row_symb_for_coord
                
                in_cell = self.in_cell_symb((j, i))
                
                coord_for_col = (j, i)
                col_symb_for_coord = self.col_symb(in_cell, coord_for_col)
                col_line += col_symb_for_coord
                
            print(row_line)
            print(col_line)
            
        print("  " + "-" * (self.board_size * 4 + 1))
        
    @staticmethod
    def pring_board(board):
        ui_board = UIBoard(
            board_size = board.grid_size,
            fences_horizontal = board.fences_horizontal, 
            fences_vertical = board.fences_vertical,
            player_positions = board.player_positions
        )
        ui_board.print()

def left(coord):
    return (coord[0] - 1, coord[1])

def right(coord):
    return (coord[0] + 1, coord[1])

def up(coord):
    return (coord[0], coord[1] - 1)

def down(coord):
    return (coord[0], coord[1] + 1)