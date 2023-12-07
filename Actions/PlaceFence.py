from Protocols import Action

class PlaceFence(Action):
    
    def __init__(self, isHorizontal: bool, coord: (int, int)):
        self.isHorizontal = isHorizontal
        self.coord = coord
        
    def __eq__(self, other):
        return self.isHorizontal == other.isHorizontal and self.coord == other.coord
    
    def __hash__(self):
        return hash((self.isHorizontal, self.coord))
    
    def __repr__(self):
        direction = "H" if self.isHorizontal else "V"
        return f"PlaceFence | {direction} at {self.coord}"