from Core import Player

class UIBoard:
    def __init__(self, board_size = 9, fences_horizontal = set(), fences_vertical = set(), player_positions = {
            Player.MAX: (4, 0),
            Player.MIN: (4, 8),
        }):
        self.board_size = board_size
        self.fences_horizontal = fences_horizontal
        self.fences_vertical = fences_vertical
        self.player_positions = player_positions

    def draw(self):
        for y in range(self.board_size):
            for x in range(self.board_size):
                # Print player positions
                if (x, y) == self.player_positions[Player.MAX]:
                    print('■', end=' ')
                elif (x, y) == self.player_positions[Player.MIN]:
                    print('●', end=' ')
                else:
                    print('.', end=' ')

                # Print vertical fences
                if (x, y) in self.fences_vertical:
                    print('|', end=' ')
                else:
                    print(' ', end=' ')

            print()

            # Print horizontal fences
            for x in range(self.board_size):
                if (x, y) in self.fences_horizontal:
                    print('—————', end=' ')
                else:
                    print('   ', end=' ')
            print()
