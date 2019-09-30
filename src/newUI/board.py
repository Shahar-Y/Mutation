import math
import os
import random
import pygame
from enums import Step, int_to_step
import constants as C

ALGEA = pygame.image.load(os.path.join(os.getcwd(), 'src/newUI/images/algea.png'))

def distance(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)

def get_nearest_food(cell, foods):
    closesd_food = foods[0]
    closest_distance = math.hypot(cell.x - foods[0].x, cell.y - foods[0].y)
    for _, food in enumerate(foods):
        dist = math.hypot(cell.x - food.x, cell.y - food.y)
        if closest_distance > dist:
            closest_distance = dist
            closesd_food = food
    return closesd_food

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


class Cell(object):
    def __init__(self, x, y, width, height, char):
        self.x = x
        self.y = y
        self.size = 20
        self.width = width
        self.height = height
        self.vel = C.INIT_VEL
        self.direction = Step.UP
        self.char = char

    def draw(self, win):
        win.blit(self.char, (self.x, self.y))

    def check_collision(self, food):
        d = math.hypot(self.x - food.x, self.y - food.y)
        if d < self.size + food.size:
            print("EATEN! d=", d, " ", self.size, " + ", food.size)

    def move(self, foods):
        dirs = []

        if len(foods) != 0:
            food = get_nearest_food(self, foods)
            if food.x < self.x:
                dirs.append(Step.LEFT)
            if food.x > self.x:
                dirs.append(Step.RIGHT)
            if food.y < self.y:
                dirs.append(Step.UP)
            if food.y > self.y:
                dirs.append(Step.DOWN)
            random.shuffle(dirs)
            if len(dirs) != 0:
                self.direction = dirs[0]
        else:
            change_dir = random.randint(0, 5)
            if change_dir == 0:
                rand_num = random.randint(0, 3)
                self.direction = int_to_step(rand_num)
        
        if self.direction == Step.LEFT and self.x > 0:
            self.x -= self.vel
        if self.direction == Step.RIGHT and self.x < C.BORDERS - self.width:
            self.x += self.vel
        if self.direction == Step.UP and self.y > 0:
            self.y -= self.vel
        if self.direction == Step.DOWN and self.y < C.BORDERS - self.height:
            self.y += self.vel

        
board = Board(500)
board.add_food(100,100)

print(board.get_closest_food(20,20).print())
