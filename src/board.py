import math
import os
import random
from functools import reduce
import pygame
from enums import Step, int_to_step
import constants as C

ALGEA = pygame.image.load(os.path.join(os.getcwd(), 'src/images/small_food.png'))

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

def first_smallest(val1, val2):
    if val1[0] < val2[0]:
        return val1
    return val2

class Board():
    def __init__(self):
        self.cells = []
        self.foods = []

    def get_nearest_food(self, cell):
        closest_food = None
        cf_idx = None
        is_food = True
        closest_distance = float('inf')
        sight_distance = cell.sight*C.SIGHT_WORTH
        mapy = map(cell.get_distance, self.foods)
        red = reduce(lambda a, b: a if first_smallest(a, b) else b, mapy)
        for i, food in enumerate(self.foods):
            if abs(cell.x - food.x > sight_distance) or abs(cell.y - food.y > sight_distance):
                continue
            dist = math.hypot(cell.x - food.x, cell.y - food.y)
            if sight_distance > dist and closest_distance > dist:
                closest_distance = dist
                closest_food = food
                cf_idx = i
        # if red != closest_distance:
            # print(str(red)+ " vs " + str(closest_distance))
        for j, second_cell in enumerate(self.cells):
            if abs(cell.x - second_cell.x > sight_distance) or abs(cell.y - second_cell.y > sight_distance):
                continue
            if cell.size >= second_cell.size + C.EATING_SIZE:
                dist = math.hypot(cell.x - second_cell.x, cell.y - second_cell.y)
                if sight_distance > dist and closest_distance > dist:
                    closest_distance = dist
                    closest_food = second_cell
                    cf_idx = j
                    is_food = False


        return closest_food, cf_idx, is_food

    def add_food(self, x, y):
        self.foods.append(Food(x, y))

    def add_cell(self, rcell):
        new_cell = Cell.duplicate_cell(rcell)
        new_cell.mutate()
        self.cells.append(new_cell)
        # txt = ''
        # for c in self.cells:
        #     txt += '[' + str(c.sight) + ','+str(c.vel) + ','+ str(c.size) + '] '
        # print(txt)




    def make_step(self):
        for i, curr_cell in enumerate(self.cells):
            curr_cell.hunger -= 1
            nearest_food = None
            if curr_cell.hunger <= 0:
                self.cells.pop(i)
            if not curr_cell.full:
                nearest_food, _, is_food = self.get_nearest_food(curr_cell)
            curr_cell.move(nearest_food)
            if nearest_food:
                eaten = curr_cell.check_eaten(nearest_food)
                if eaten:
                    curr_cell.hunger += curr_cell.food_worth
                    if curr_cell.hunger >= C.FULL_HUNHER:
                        curr_cell.full = True
                    if is_food:
                        self.foods.remove(nearest_food)
                    else: 
                        self.cells.remove(nearest_food)
                    if curr_cell.pregnency == curr_cell.repro_rate:
                        curr_cell.pregnency = 0
                        curr_cell.hunger = int(curr_cell.hunger*2/3)
                        self.add_cell(curr_cell)
            else: 
                if curr_cell.hunger <= C.HUNGRY_HUNGER:
                    curr_cell.full = False            



class Cell(object):
    def __init__(self, x, y, hunger, size, sight, vel):
        self.x = x
        self.y = y
        self.hunger = hunger
        self.full = False

        self.size = size
        self.sight = sight
        self.vel = vel


        self.direction = Step.UP
        self.pregnency = 0

        self.repro_rate = 'None'
        self.food_worth = 'None'
        self.icon = 'None'
        self.char = 'None'
        self.set_icon_path()
        self.set_char()
        self.set_food_reference()

    @classmethod
    def duplicate_cell(cls, cell) -> 'Cell':
        return  cls(x=cell.x, y=cell.y, hunger=cell.hunger, size=cell.size,
                    sight=cell.sight, vel=cell.vel)

    def draw(self, win):
        win.blit(self.char, (self.x, self.y))

    def check_eaten(self, food):
        dist = math.hypot(self.x - food.x, self.y - food.y)
        if dist < C.EATING_DISTANCE:
            self.pregnency += 1
            return True
        return False

    def get_mutation_points(self):
        return self.vel + self.sight + self.size

    def get_distance(self, point):
        return (math.hypot(point.x - self.x, point.y - self.y), point)

    def set_icon_path(self):
        self.icon = 'src/images/icons/Cell_'+str(self.sight)+'_'+str(self.vel)+'_'+str(self.size)+'.png'

    def set_char(self):
        self.char = pygame.image.load(os.path.join(os.getcwd(), self.icon))

    def mutate(self):
        mutation_chance = random.randint(1, C.MUTATION_CHANCE)
        if mutation_chance == 1:
            mutation = random.randint(-1, 1)
            if self.sight+mutation <= C.MAX_SIGHT and self.sight+mutation >= C.MIN_SIGHT:
                if self.get_mutation_points()+mutation <= C.MAX_MUTATION_POINTS:
                    self.sight += mutation

            mutation = random.randint(-1, 1)
            if self.size+mutation <= C.MAX_SIZE and self.size+mutation >= C.MIN_SIZE:
                if self.get_mutation_points()+mutation <= C.MAX_MUTATION_POINTS:
                    self.size += mutation

            mutation = random.randint(-1, 1)
            if (self.vel+mutation <= C.MAX_VEL) and (self.vel+mutation >= C.MIN_VEL):
                if self.get_mutation_points()+mutation < C.MAX_MUTATION_POINTS:
                    self.vel = self.vel + mutation

            self.set_icon_path()
            self.set_char()
            self.set_food_reference()

    def set_food_reference(self):
        self.repro_rate = int(self.size/2) + 2
        self.food_worth = 70

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
        if self.direction == Step.RIGHT and self.x < C.WINDOW_WIDTH - self.size*2:
            self.x += self.vel
        if self.direction == Step.UP and self.y > 0:
            self.y -= self.vel
        if self.direction == Step.DOWN and self.y < C.WINDOW_HEIGHT - self.size*2:
            self.y += self.vel
