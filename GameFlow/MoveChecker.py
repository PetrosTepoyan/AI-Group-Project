from Core import Player

class MoveChecker:
    
    def __init__(self, board_size):
        self.board_size = board_size

    def is_within_board(self, coord):
        x, y = coord
        return 0 <= x < self.board_size and 0 <= y < self.board_size

    def is_fence_blocking(self, from_coord, to_coord, fences_horizontal, fences_vertical):
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
        if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
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

