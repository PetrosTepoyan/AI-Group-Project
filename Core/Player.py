from enum import Enum, auto

class Player(Enum):
    """`Player` class discerns between the MAX and MIN actors in the game"""
    MAX = auto()
    MIN = auto()

    def toggle(self) -> 'Player':
        """Toggles actor's type from MIN to MAX and vice versa"""
        if self == Player.MAX:
            return Player.MIN
        return Player.MAX
