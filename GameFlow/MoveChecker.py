from GameFlow import Board

class MoveChecker:
    """`MoveChecker` verifies validity and performs operations concerning player movement"""
    def __init__(self, grid_size: int) -> None:
        self.grid_size = grid_size
        self.board = None

    def set_board(self, board: Board) -> None:
        """Associate checker with a board"""
        self.board = board

    def get_movable_coords(self, player_coord=None, opponent_coord=None) -> set[tuple[int, int]]:
        """Returns a set of coordinates a player can move to in a board"""
        if player_coord is None:
            player_coord = self.board.player_positions[self.board.current_player]
        if opponent_coord is None:
            opponent_coord = self.board.player_positions[self.board.current_opponent]
        movable_coords = set()
        # Check all four directions: left, right, up, down
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_coord = (player_coord[0] + dx, player_coord[1] + dy)
            is_blocking_fence = self.is_fence_blocking(player_coord, next_coord)
            # print(f"next coord is {next_coord}, is it blocked by fence? {is_blocking_fence}")
            if self.is_within_board(next_coord) and not is_blocking_fence:
                jumping_coords_if_any = self.jump_over_coords(player_coord, opponent_coord)
                movable_coords = movable_coords | jumping_coords_if_any

                if next_coord != opponent_coord:
                    movable_coords.add(next_coord)

        return movable_coords

    def jump_over_coords(self, player_coord=None, opponent_coord=None) -> set[tuple[int, int]]:
        """Returns a set of coordinates a player can reach if they jump over the opponent, with
        a priority given to direct jumps"""
        if player_coord is None:
            player_coord = self.board.player_positions[self.board.current_player]
        if opponent_coord is None:
            opponent_coord = self.board.player_positions[self.board.current_opponent]

        if self.is_fence_blocking(player_coord, opponent_coord):
            return set()

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
            is_direct_jump_not_blocked = not self.is_fence_blocking(opponent_coord, jump_coord_direct)
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
                is_diag_jump_not_blocked = not self.is_fence_blocking(opponent_coord, jump_coord)
                if is_diag_jump_in_board and is_diag_jump_not_blocked:
                    return_coords.add(jump_coord)

            return return_coords

        if player_coord[0] == opponent_coord[0]: # vertically jumping
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
            is_direct_jump_not_blocked = not self.is_fence_blocking(opponent_coord, jump_coord_direct)

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
                is_diag_jump_blocked = self.is_fence_blocking(opponent_coord, jump_coord)
                if is_diag_jump_in_board and not is_diag_jump_blocked:
                    return_coords.add(jump_coord)

            return return_coords

        return set()

    def is_within_board(self, coord) -> bool:
        """Returns true if the coordinate is within the board, false otherwise"""
        x, y = coord
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size

    def is_fence_blocking(self, from_coord, to_coord) -> bool:
        """Returns true if adjacent cells are blocked by a fence; false otherwise"""
        if from_coord[0] == to_coord[0]:  # Vertical movement
            if to_coord == up(from_coord): # going up
                return ((to_coord in self.board.fences_horizontal) or (left(to_coord) in self.board.fences_horizontal))
            if to_coord == down(from_coord): # going down
                return (from_coord in self.board.fences_horizontal) or (left(from_coord) in self.board.fences_horizontal)
        else:  # Horizontal movement
            if to_coord == right(from_coord): # going right:
                return (from_coord in self.board.fences_vertical) or (up(from_coord) in self.board.fences_vertical)
            if to_coord == left(from_coord): # going left
                return (to_coord in self.board.fences_vertical) or (up(to_coord) in self.board.fences_vertical)

def left(coord) -> tuple[int, int]:
    """Return coordinates of the cell to the left"""
    return (coord[0] - 1, coord[1])

def right(coord) -> tuple[int, int]:
    """Return coordinates of the cell to the right"""
    return (coord[0] + 1, coord[1])

def up(coord) -> tuple[int, int]:
    """Return coordinates of the cell above"""
    return (coord[0], coord[1] - 1)

def down(coord) -> tuple[int, int]:
    """Return coordinates of the cell below"""
    return (coord[0], coord[1] + 1)
