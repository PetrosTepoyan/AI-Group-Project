from enum import Enum, auto

class Player(Enum):
    MAX = auto()
    MIN = auto()
    
    def toggle(self):
        if self == Player.MAX:
            return Player.MIN
        else:
            return Player.MAX
