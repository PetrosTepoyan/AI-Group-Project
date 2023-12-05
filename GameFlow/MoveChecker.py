from Core import Player

class MoveChecker:
    
    def __init__(self, board_size):
        self.board_size = board_size

    def is_within_board(self, coord):
        x, y = coord
        return 0 <= x < self.board_size and 0 <= y < self.board_size

    def is_fence_blocking(self, from_coord, to_coord, fences_horizontal, fences_vertical):
        # print(from_coord , to_coord, fences_horizontal, fences_vertical)
        if from_coord[0] == to_coord[0]:  # Horizontal movement
            row = from_coord[0]
            col_min = min(from_coord[1], to_coord[1])
            return ((row, col_min) in fences_horizontal)
        else:  # Vertical movement
            col = from_coord[1]
            row_min = min(from_coord[0], to_coord[0])
            return ((row_min, col) in fences_vertical)

    def can_move(self, player, to_coord, fences_horizontal, fences_vertical, player_positions):
        from_coord = player_positions[player]
        # Ensure target coordinate is adjacent and within board bounds
        if not self.is_within_board(to_coord):
            return False
        # Check if movement is one space in any direction
        dx = abs(from_coord[0] - to_coord[0])
        dy = abs(from_coord[1] - to_coord[1])
        if (dx + dy == 1):
            # Check if there is a fence blocking the movement
            if self.is_fence_blocking(from_coord, to_coord, fences_horizontal, fences_vertical):
                return False
            # Check if moving to a space occupied by the opponent
            opponent = Player.MAX if player == Player.MIN else Player.MIN
            if to_coord == player_positions[opponent]:
                # Need to check for jump conditions
                return self.can_jump_over(player, opponent)
            return True
        return False

    def can_jump_over(self, player, opponent, fences_horizontal, fences_vertical, player_positions):
        # Check if player can jump over the opponent (including diagonal jumps if next to a fence)
        player_coord = player_positions[player]
        opponent_coord = player_positions[opponent]

        # # Horizontally aligned
        # if player_coord[1] == opponent_coord[1]:
        #     # Player is on the right of the opponent
        #     if player_coord[0] > opponent_coord[1]:
        #         v_fence_1 = (opponent_coord[0] - 1, opponent_coord[1])
        #         v_fence_2 = (opponent_coord[0] - 1, opponent_coord[1] - 1)
        #         if v_fence_1 in fences_vertical or v_fence_2 in fences_vertical:
        #             return False

        # Simple forward jump
        if player_coord[1] == opponent_coord[1]:
            jump_coord = (opponent_coord[0] + (opponent_coord[0] - player_coord[0]), opponent_coord[1])
            if self.is_within_board(jump_coord) and not self.is_fence_blocking(opponent_coord, jump_coord, fences_horizontal, fences_vertical):
                return True

        # Lateral jumps due to a blocking fence
        for dx in [-1, 1]:
            side_jump_coord = (opponent_coord[0], opponent_coord[1] + dx)
            if self.is_within_board(side_jump_coord) and not self.is_fence_blocking(player_coord, side_jump_coord, fences_horizontal, fences_vertical):
                return True

        # Diagonal jump checks
        player_coord = player_positions[player]
        opponent_coord = player_positions[opponent]
        
        # Check if the opponent is directly in front and there is a fence blocking a straight jump
        straight_jump_blocked = self.is_fence_blocking(player_coord, opponent_coord, fences_horizontal, fences_vertical)
        
        if straight_jump_blocked:
            for dx, dy in [(-1, 1), (1, 1), (-1, -1), (1, -1)]:
                # Calculate the diagonal jump coordinates
                diag_jump_coord = (opponent_coord[0] + dx, opponent_coord[1] + dy)
                
                # Check if the diagonal jump is within the board and not blocked by a fence
                if self.is_within_board(diag_jump_coord):
                    fence_side_check = (opponent_coord[0], opponent_coord[1] + dy if dx == 0 else opponent_coord[1])
                    fence_back_check = (opponent_coord[0] + dx if dy == 0 else opponent_coord[0], opponent_coord[1])
                    if (not self.is_fence_blocking(opponent_coord, fence_side_check) and
                            not self.is_fence_blocking(opponent_coord, fence_back_check, fences_horizontal, fences_vertical)):
                        return True
                    
        return False

    def get_movable_coords(
        self,
        player: Player,
        opponent: Player,
        fences_horizontal: set,
        fences_vertical: set, 
        player_positions
    ):
        player_coords = player_positions[player]
        opponent_coords = player_positions[opponent]
        
        movable_coords: set = set() 
        
        left = (player_coords[0] - 1, player_coords[1])
        left_up = (player_coords[0] - 1, player_coords[1] - 1)
        left_down = (player_coords[0] - 1, player_coords[1] + 1)
        
        # Is in within the board
        if self.is_within_board(left):
            # If there is an immediate fence, we should check if we can go diagonally
            if self.is_fence_blocking(player_coords, left, fences_horizontal, fences_vertical):
                 # Is in within the board
                 # and if there a fence that blocks that path too
                if self.is_within_board(left_up) and \
                    not self.is_fence_blocking(opponent_coords, left_up, fences_horizontal, fences_vertical):
                    movable_coords.add(left_up)
                    
                if self.is_within_board(left_down) and \
                    not self.is_fence_blocking(opponent_coords, left_down, fences_horizontal, fences_vertical):
                    movable_coords.add(left_down)
                    
            # If there is no an immediate fence, we can go there right away
            else:
                movable_coords.add(left)
                
    def get_movable_coords_G(
        self,
        player: Player,
        opponent: Player,
        fences_horizontal: set,
        fences_vertical: set, 
        player_positions
    ):
        player_coords = player_positions[player]
        opponent_coords = player_positions[opponent]
        
        movable_coords: set = set() 

        # Check all four directions: left, right, up, down
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_coord = (player_coords[0] + dx, player_coords[1] + dy)

            if self.is_within_board(next_coord):
                if self.is_fence_blocking(player_coords, next_coord, fences_horizontal, fences_vertical):
                    # Check for diagonal moves in case of a blocking fence
                    for ddx, ddy in [(-dx, dy), (dx, dy)]:
                        diag_coord = (player_coords[0] + ddx, player_coords[1] + ddy)
                        if self.is_within_board(diag_coord) and not self.is_fence_blocking(opponent_coords, diag_coord, fences_horizontal, fences_vertical):
                            movable_coords.add(diag_coord)
                else:
                    movable_coords.add(next_coord)
                    
        # Check for jump possibilities
        if self.can_jump_over(player, opponent, fences_horizontal, fences_vertical, player_positions):
            jump_dx = opponent_coords[0] - player_coords[0]
            jump_dy = opponent_coords[1] - player_coords[1]
            jump_coord = (opponent_coords[0] + jump_dx, opponent_coords[1] + jump_dy)
            if self.is_within_board(jump_coord) and not self.is_fence_blocking(opponent_coords, jump_coord, fences_horizontal, fences_vertical):
                movable_coords.add(jump_coord)

        return movable_coords
