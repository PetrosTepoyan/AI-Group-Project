import Core.Player as Player
from Protocols import Action

class State:
    
    def get_player(self) -> Player:
        pass

    def get_applicable_actions(self):
        pass

    def get_action_result(self, action: Action):
        pass
    
    def __eq__(self, other):
        pass
    
    def __hash__(self):
        pass