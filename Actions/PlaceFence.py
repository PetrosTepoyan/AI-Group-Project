from Protocols import Action

class PlaceFence(Action):
    "`PlaceFence` is an `Action` class responsible for placing a fence on the board"
    def __init__(self, is_horizontal: bool, coord: (int, int)):
        self.is_horizontal = is_horizontal
        self.coord = coord

    def __eq__(self, other):
        return self.is_horizontal == other.is_horizontal and self.coord == other.coord

    def __hash__(self):
        return hash((self.is_horizontal, self.coord))

    def __repr__(self):
        direction = "H" if self.is_horizontal else "V"
        return f"PlaceFence | {direction} at {self.coord}"
