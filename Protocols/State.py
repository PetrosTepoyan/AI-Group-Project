import Core.Player as Player
from GameFlow import Board
from Protocols import Action

class State:
    def get_player(self) -> Player:
        """Get the player agent type"""

    def get_applicable_actions(self) -> list[Action]:
        """Get a list of valid actions"""

    def get_action_result(self, action: Action) -> Board:
        """Get a state after applying the action"""

    def __eq__(self, other):
        pass

    def __hash__(self):
        pass
