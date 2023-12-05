
from Core.Player import Player
from Protocols import Action, State
from Actions import Move, PlaceFence
from GameFlow import FenceChecker, MoveChecker

class Board(State):
    
    def __init__(
        self,
        fence_checker: FenceChecker,
        move_checker: MoveChecker,
        grid_size = 9,
        player_positions: dict = None,
        current_player: Player = Player.MAX,
        fences_horizontal = set(),
        fences_vertical = set()
    ):
        
        self.fence_checker = fence_checker
        self.move_checker = move_checker
        self.grid_size = grid_size
        mid_point = grid_size // 2  
        if player_positions is None:
            self.player_positions = {
                Player.MAX: (mid_point, 0),            # Player.MAX starts at the top row
                Player.MIN: (mid_point, grid_size-1)   # Player.MIN starts at the bottom row
            }
        else:
            self.player_positions = player_positions
            
        self.current_player = current_player
        self.fences_horizontal = fences_horizontal
        self.fences_vertical = fences_vertical

    def get_player(self) -> Player:
        return self.current_player
    
    def toggle_player(self):
        self.current_player = self.current_player.toggle()
    
    def get_applicable_actions(self):
        actions = []
        # Calculate possible moves for the pawn
        current_pos = self.player_positions[self.get_player()]
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # down, right, up, left
            new_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
            if self.is_move_valid(current_pos, new_pos):
                actions.append(Move(current_pos, new_pos))
        
        # Calculate possible fence placements
        for i in range(self.grid_size - 1):
            for j in range(self.grid_size - 1):
                if self.can_place_fence((i, j), True):
                    actions.append(PlaceFence(True, (i, j)))
                if self.can_place_fence((i, j), False):
                    actions.append(PlaceFence(False, (i, j)))

        return actions

    def get_action_result(self, action: Action):
        new_board = Board(
            fence_checker = self.fence_checker,
            move_checker = self.move_checker,
            grid_size = self.grid_size,
            player_positions = self.player_positions,
            current_player = self.current_player,
            fences_horizontal = self.fences_horizontal,
            fences_vertical = self.fences_vertical
        )
        if isinstance(action, Move):
            # Assume it's the current player's move
            new_board.player_positions[new_board.get_player()] = action.to_coord
        elif isinstance(action, PlaceFence):
            new_board.fences.add((action.isHorizontal, action.coord))
        
        new_board.toggle_player()  # Switch to the other player
        
        return new_board
    
    def is_move_valid(self, from_coord, to_coord):
        # Add logic to check if the move is valid (e.g., not blocked by a fence).
        return True

    def can_place_fence(self, coord, is_horizontal):
        # Add logic to check if a fence can be placed (not already placed, not blocking a path).
        self.fences
        return True
    
    def __eq__(self, other):
        if isinstance(other, Board):
            return (self.player_positions == other.player_positions and
                    self.fences == other.fences and
                    self.current_player == other.current_player)
        return False
    
    def __hash__(self):
        return hash((frozenset(self.player_positions.items()), frozenset(self.fences), self.current_player))
