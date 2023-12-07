from Protocols import Action

class Move(Action):
    
    def __init__(self, from_coord: (int, int), to_coord: (int, int)):
        self.from_coord = from_coord
        self.to_coord = to_coord
        
    def __repr__(self):
        return f"Move | {self.from_coord} {self.to_coord}"
        
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.from_coord == other.from_coord and self.to_coord == other.to_coord
        return False
    
    def __hash__(self):
        return hash((self.from_coord, self.to_coord))