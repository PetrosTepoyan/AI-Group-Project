from Core import Player

class UIBoard:
    def __init__(self, board_size = 9, fences_horizontal = set(), fences_vertical = set(), player_positions = {
            Player.MAX: (4, 0),
            Player.MIN: (4, 8),
        }, current_player: Player = Player.MAX):
        self.board_size = board_size
        self.fences_horizontal = fences_horizontal
        self.fences_vertical = fences_vertical
        self.player_positions = { value : ("X" if key == Player.MAX else "O") for key, value in player_positions.items()}
        self.current_player = current_player

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
            
            is_bold = self.player_positions[coord] == "X" and self.current_player == Player.MAX 
            is_bold = is_bold or (self.player_positions[coord] == "O" and self.current_player == Player.MIN)
            
            return ('\033[91m' + in_cell + '\033[0m') if is_bold else in_cell

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
        
    def string(self):
        board_str = ""
        board_str += "    " + "   ".join([str(i) for i in range(self.board_size)]) + "\n"
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

            board_str += row_line + "\n"
            board_str += col_line + "\n"

        board_str += "  " + "-" * (self.board_size * 4 + 1) + "\n"
        return board_str
   
    @staticmethod
    def string_board(board):
        ui_board = UIBoard(
            board_size = board.grid_size,
            fences_horizontal = board.fences_horizontal, 
            fences_vertical = board.fences_vertical,
            player_positions = board.player_positions,
            current_player= board.current_player
        )
        return ui_board.string()
        
    @staticmethod
    def print_board(board):
        ui_board = UIBoard(
            board_size = board.grid_size,
            fences_horizontal = board.fences_horizontal, 
            fences_vertical = board.fences_vertical,
            player_positions = board.player_positions,
            current_player= board.current_player
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