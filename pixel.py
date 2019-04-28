from enum import Enum, auto


class PixelType(Enum):
    Pixel = auto()
    Cell = auto()
    Food = auto()
    Rock = auto()
    Antibiotics = auto()


class Pixel:
    def __init__(self, width, length):
        self.length = length
        self.width = width
        self.x = 0
        self.y = 0
        self.type = PixelType.Pixel

    def inc_size(self):
        self.length += 1
        self.width += 1

    def print_cell(self):
        print("*******************************")
        print("pixel type: " + str(self.type))
        print("pixel length: " + str(self.length) + ", width: " + str(self.width))
        print("pixel location: " + str(self.x) + "," + str(self.y))
        print("*******************************")
