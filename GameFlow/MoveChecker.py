from Core import Player

class MoveChecker:
    
    def __init__(self, grid_size):
        self.board_size = grid_size

    def get_movable_coords(self, player, opponent, fences_horizontal, fences_vertical, player_positions):

        player_coord = player_positions[player]
        opponent_coord = player_positions[opponent]
        movable_coords = set()

        # Check all four directions: left, right, up, down
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_coord = (player_coord[0] + dx, player_coord[1] + dy)
            is_blocking_fence = self.is_fence_blocking(player_coord, next_coord, fences_horizontal, fences_vertical)
            if self.is_within_board(next_coord) and not is_blocking_fence:
                jumping_coords_if_any = self.jump_over_coords(
                    player,
                    opponent,
                    fences_horizontal,
                    fences_vertical,
                    player_positions
                )
                movable_coords = movable_coords | jumping_coords_if_any
                
                if next_coord != opponent_coord:
                    movable_coords.add(next_coord)

        return movable_coords

    def is_within_board(self, coord):
            x, y = coord
            return 0 <= x < self.board_size and 0 <= y < self.board_size

    def is_fence_blocking(self, from_coord, to_coord, fences_horizontal, fences_vertical):
        if from_coord[0] == to_coord[0]:  # Vertical movement
            return (from_coord in fences_horizontal) or (left(from_coord) in fences_horizontal)
        else:  # Horizontal movement
            if to_coord == right(from_coord): # going right:
                return (from_coord in fences_vertical) or (up(from_coord) in fences_vertical)
            elif to_coord == left(from_coord):
                return (to_coord in fences_vertical) or (up(to_coord) in fences_vertical)

    def jump_over_coords(self, player, opponent, fences_horizontal, fences_vertical, player_positions):
        player_coord = player_positions[player]
        opponent_coord = player_positions[opponent]
        
        if player_coord[1] == opponent_coord[1]: # horizontally jumping
            if player_coord[0] == left(opponent_coord)[0]: # player is to the left
                jump_coord_direct = (
                    opponent_coord[0] + 1,
                    player_coord[1]
                )
            elif player_coord[0] == right(opponent_coord)[0]:
                jump_coord_direct = (
                    opponent_coord[0] - 1,
                    player_coord[1]
                )
            else: # not next to each other
                return set()
            
            is_direct_jump_in_board = self.is_within_board(jump_coord_direct)
            is_direct_jump_not_blocked = not self.is_fence_blocking(
                opponent_coord, jump_coord_direct,
                fences_horizontal, fences_vertical
            )
            if is_direct_jump_in_board and is_direct_jump_not_blocked:
                 # if able to jump directly, do so
                return set([jump_coord_direct])
            
            # otherwise, try diag jump
            jump_coord_up = (
                opponent_coord[0],
                opponent_coord[1] - 1
            )
            
            jump_coord_down = (
                opponent_coord[0],
                opponent_coord[1] + 1
            )
            return_coords = set()
            for jump_coord in [jump_coord_up, jump_coord_down]:
                is_diag_jump_in_board = self.is_within_board(jump_coord)
                is_diag_jump_not_blocked = not self.is_fence_blocking(
                    opponent_coord, jump_coord,
                    fences_horizontal, fences_vertical
                )
                if is_diag_jump_in_board and is_diag_jump_not_blocked:
                    return_coords.add(jump_coord)
                    
            return return_coords
        
        elif player_coord[0] == opponent_coord[0]: # vertically jumping
            if player_coord[1] == up(opponent_coord)[1]: # player is above
                jump_coord_direct = (
                    opponent_coord[0],
                    opponent_coord[1] + 1
                )
                
            elif player_coord[1] == down(opponent_coord)[1]:
                jump_coord_direct = (
                    opponent_coord[0],
                    opponent_coord[1] - 1
                )
            else:
                return set()
            
            is_direct_jump_in_board = self.is_within_board(jump_coord_direct)
            is_direct_jump_not_blocked = not self.is_fence_blocking(
                opponent_coord, jump_coord_direct,
                fences_horizontal, fences_vertical
            )
            
            if is_direct_jump_in_board and is_direct_jump_not_blocked:
                 # if able to jump directly, do so
                return set([jump_coord_direct])
            
            # otherwise, try diag jump
            jump_coord_left = left(opponent_coord)
            jump_coord_right = right(opponent_coord)
            
            return_coords = set()
            # print()
            for jump_coord in [jump_coord_left, jump_coord_right]:
                is_diag_jump_in_board = self.is_within_board(jump_coord)
                is_diag_jump_blocked = self.is_fence_blocking(
                    opponent_coord, jump_coord,
                    fences_horizontal, fences_vertical
                )
                # print("TT", opponent_coord, jump_coord, is_diag_jump_in_board, is_diag_jump_blocked, fences_vertical)
                
                if is_diag_jump_in_board and not is_diag_jump_blocked:
                    return_coords.add(jump_coord)
                    
            return return_coords
            
            
        return set()

def left(coord):
    return (coord[0] - 1, coord[1])

def right(coord):
    return (coord[0] + 1, coord[1])

def up(coord):
    return (coord[0], coord[1] - 1)

def down(coord):
    return (coord[0], coord[1] + 1)