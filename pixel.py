
class Pixel:
    def __init__(self, width, length):
        self.length = length
        self.width = width

    def incSize(self):
        self.length += 1
        self.width += 1

    def printCell(self):
        print("pixel length: " + str(p1.length) + ", width: " + str(p1.width))

p1 = Pixel(5, 10)
p1.printCell()
p1.incSize()
p1.printCell()
