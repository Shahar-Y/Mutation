import math
import os
import pygame

ALGEA = pygame.image.load(os.path.join(os.getcwd(), 'src/newUI/images/algea.png'))

def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))

class Food():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20

    def print(self):
        print('x: ' + str(self.x) + ', y: ' + str(self.y))

    def draw(self, win):
        win.blit(ALGEA, (self.x, self.y))

class Board():
    def __init__(self, size):
        self.size = size
        self.cells = []
        self.food = []

    def get_closest_food(self, x, y):
        closest_distance = 2*self.size
        closest_food = None

        for food in self.food:
            dis = distance(x, y, food.x, food.y)
            if dis < closest_distance:
                dis = closest_distance
                closest_food = food

        return closest_food

    def add_food(self, x, y):
        self.food.append(Food(x, y))


        
board = Board(500)
board.add_food(100,100)

print(board.get_closest_food(20,20).print())
