import math
import os
import random
import pygame
from enums import Step, int_to_step
import constants as C

ALGEA = pygame.image.load(os.path.join(os.getcwd(), 'src/newUI/images/algea.png'))

def distance(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)

class Food():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = C.FOOD_SIZE

    def print(self):
        print('x: ' + str(self.x) + ', y: ' + str(self.y))

    def draw(self, win):
        win.blit(ALGEA, (self.x, self.y))

class Board():
    def __init__(self):
        self.cells = []
        self.foods = []

    def get_nearest_food(self, cell):
        closesd_food = None
        cf_idx = None
        closest_distance = float('inf')
        for i, food in enumerate(self.foods):
            dist = math.hypot(cell.x - food.x, cell.y - food.y)
            if closest_distance > dist:
                closest_distance = dist
                closesd_food = food
                cf_idx = i
        return closesd_food, cf_idx

    def add_food(self, x, y):
        self.foods.append(Food(x, y))

    def add_cell(self, cell):
        new_cell = Cell.duplicate_cell(cell)
        new_cell.hunger = int(new_cell.hunger/2)
        self.cells.append(new_cell)

    def make_step(self):
        for curr_cell in self.cells:
            curr_cell.hunger -= 1
            if curr_cell.hunger <= 0:
                self.cells.remove(curr_cell)
            nearest_food, _ = self.get_nearest_food(curr_cell)
            curr_cell.move(nearest_food)
            if nearest_food:
                eaten = curr_cell.check_eaten(nearest_food)
                if eaten:
                    curr_cell.hunger += 20
                    self.foods.remove(nearest_food)
                    if curr_cell.pregnency == curr_cell.repro_rate:
                        curr_cell.pregnency = 0
                        curr_cell.hunger = int(curr_cell.hunger/2)
                        self.reproduce(curr_cell)

    def reproduce(self, cell):
        self.add_cell(cell)
        print(len(self.cells), "  ", len(self.foods), str(len(self.cells)*len(self.foods)))


class Cell(object):
    def __init__(self, x, y, width, height, char, hunger):
        self.x = x
        self.y = y
        self.size = C.INIT_SIZE
        self.width = width
        self.height = height
        self.vel = C.INIT_VEL
        self.direction = Step.UP
        self.char = char
        self.pregnency = 0
        self.repro_rate = C.INIT_FOOD_TO_REPRO
        self.hunger = hunger

    @classmethod
    def duplicate_cell(cls, cell) -> 'Cell':
        return  cls(x=cell.x, y=cell.y, width=cell.width, height=cell.height,
                    char=cell.char, hunger=cell.hunger)

    def draw(self, win):
        win.blit(self.char, (self.x, self.y))

    def check_eaten(self, food):
        dist = math.hypot(self.x - food.x, self.y - food.y)
        if dist < C.EATING_DISTANCE:
            self.pregnency += 1
            return True
        return False


    def move(self, food):
        dirs = []

        if food:
            if food.x + 5 < self.x:
                dirs.append(Step.LEFT)
            if food.x - 5 > self.x:
                dirs.append(Step.RIGHT)
            if food.y + 5 < self.y:
                dirs.append(Step.UP)
            if food.y - 5 > self.y:
                dirs.append(Step.DOWN)
            random.shuffle(dirs)
            if dirs:
                self.direction = dirs[0]
        else:
            change_dir = random.randint(0, C.CHANGE_DIR_PROB)
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
