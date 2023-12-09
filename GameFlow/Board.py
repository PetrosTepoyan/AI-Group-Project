from copy import copy
from Core.Player import Player
from Protocols import Action, State
from Actions import Move, PlaceFence
from GameFlow import FenceChecker
from GameFlow import MoveChecker

class Board(State):
    """`Board` is a class representing the current `State` of Quoridor"""
    def __init__(self,
                 fence_checker: FenceChecker,
                 move_checker: MoveChecker,
                 grid_size = 9,
                 player_positions: dict = None,
                 current_player: Player = Player.MAX,
                 fences_horizontal: set[tuple[int, int]] = None,
                 fences_vertical: set[tuple[int, int]] = None,
                 disable_turn: bool = False):
        self.fence_checker = fence_checker
        self.move_checker = move_checker
        self.grid_size = grid_size
        
        mid_point = grid_size // 2
        if player_positions is None:
            self.player_positions = {
                Player.MAX: (mid_point, 0),                           # Player.MAX starts at the top row
                Player.MIN: (mid_point, grid_size - 1)   # Player.MIN starts at the bottom row
            }
        else:
            self.player_positions = player_positions
        self.current_player = current_player
        self.current_opponent = Player.MIN if current_player == Player.MAX else Player.MAX
        if fences_horizontal is None:
            fences_horizontal = set()
        self.fences_horizontal = fences_horizontal
        if fences_vertical is None:
            fences_vertical = set()
        self.fences_vertical = fences_vertical
        self.max_fences = int(self.grid_size * self.grid_size * (10 / 81))
        self.disable_turn = disable_turn
        self.grid_size = grid_size

    def get_player(self) -> Player:
        return self.current_player

    def toggle_player(self) -> None:
        """Flip players' agent from MAX to MIN and vice versa"""
        self.current_player = self.current_player.toggle()
        self.current_opponent = self.current_opponent.toggle()

    def get_applicable_actions(self) -> list[Action]:
        actions: list[Action] = []
        # Calculate possible moves for the pawn
        current_pos = self.player_positions[self.current_player]
        movable_coords = self.get_movable_coords()
        for coord in movable_coords:
            move = Move(from_coord = current_pos,
                        to_coord = coord)
            actions.append(move)
        # Calculate possible fence placements
        if ((len(self.fences_horizontal) + len(self.fences_vertical) <= self.max_fences) 
            and not self.disable_turn):
            for i in range(self.grid_size - 1):
                for j in range(self.grid_size - 1):
                    placing_coord = (i, j)
                    if self.can_place_fence(placing_coord, True):
                        action = PlaceFence(True, placing_coord)
                        actions.append(action)
                    if self.can_place_fence(placing_coord, False):
                        action = PlaceFence(False, placing_coord)
                        actions.append(action)
        return actions

    def get_action_result(self, action: Action) -> 'Board':
        new_board = Board(fence_checker = self.fence_checker,
                          move_checker = self.move_checker,
                          player_positions = copy(self.player_positions),
                          current_player = copy(self.current_player),
                          fences_horizontal = copy(self.fences_horizontal),
                          fences_vertical = copy(self.fences_vertical),
                          disable_turn=self.disable_turn)
        # print("Applied", action)
        if isinstance(action, Move):
            # Assume it's the current player's move
            new_board.player_positions[self.current_player] = action.to_coord
        elif isinstance(action, PlaceFence):
            if action.is_horizontal:
                new_board.fences_horizontal.add(action.coord)
            else:
                new_board.fences_vertical.add(action.coord)
        else:
            print("UNKNOWN ACTION", action)

        if not self.disable_turn:
            # Switch to the other player
            new_board.toggle_player()
        return new_board

    def can_place_fence(self, placing_coord, is_horizontal) -> bool:
        """Takes in a cell and fence orientation. Returns true if a fence is deployable"""
        return self.fence_checker.can_place_fence(placing_coord, is_horizontal,
                                                  fences_horizontal = self.fences_horizontal,
                                                  fences_vertical = self.fences_vertical)

    def get_movable_coords(self) -> set[tuple[int, int]]:
        """Returns a set of coordinates the current player can move to"""
        return self.move_checker.get_movable_coords(self, 
                                                    self.player_positions[self.current_player],
                                                    self.player_positions[self.current_opponent])

    def __eq__(self, other):
        if self.player_positions != other.player_positions:
            return False
        if self.fences_horizontal != other.fences_horizontal:
            return False
        if self.fences_vertical != other.fences_vertical:
            return False
        if self.current_player != other.current_player:
            return False
        return True

    def __hash__(self):
        return hash((frozenset(self.player_positions.items()),
                     frozenset(self.fences_horizontal), 
                     frozenset(self.fences_vertical),
                     self.current_player))

    def __repr__(self):
        max_p = self.player_positions[Player.MAX]
        min_p = self.player_positions[Player.MIN]
        return (f"Board {self.current_player} | MAX:{max_p} - MIN:{min_p} | "
                f"{len(self.fences_horizontal)} | {len(self.fences_vertical)}")
