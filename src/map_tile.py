# The main class for stationary things that inhabit the grid ... grass, trees, rocks and stuff.
class MapTile():
    def __init__(self, name, column, row, tile_type):
        self.type = tile_type
        self.name = name
        self.column = column
        self.row = row