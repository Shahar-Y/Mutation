from enums import PixelType


class Pixel:
    def __init__(self, width, length):
        self.length = length
        self.width = width
        self.x = 0
        self.y = 0
        self.type = PixelType.Pixel

    def __str__(self):
        return str("\n*******************************" +
                   "\ncell type: " + str(self.type) +
                   "\ncell length: " + str(self.length) + ", width: " + str(self.width) +
                   "\ncell location: " + str(self.x) + "," + str(self.y) +
                   "\n*******************************")

    def inc_size(self):
        self.length += 1
        self.width += 1
