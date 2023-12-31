from Protocols import Action

class Move(Action):
    """`Move` is an `Action` class responsible for moving a pawn from one cell to another"""
    def __init__(self, from_coord: (int, int), to_coord: (int, int)):
        self.from_coord = from_coord
        self.to_coord = to_coord

    def __repr__(self):
        return f"Move | {self.from_coord} {self.to_coord}"

    def __eq__(self, other):
        return self.from_coord == other.from_coord and self.to_coord == other.to_coord

    def __hash__(self):
        return hash((self.from_coord, self.to_coord))
