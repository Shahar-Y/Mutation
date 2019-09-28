# Code source: https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/optimization/
import random
import os
import math
import pygame
from enums import Step, int_to_step
import constants as C
from board import Board, Food

pygame.init()

WIN = pygame.display.set_mode((C.BORDERS, C.BORDERS))
# img = Image.open(os.path.join(os.getcwd(), 'src/images/cell.png'))
# basewidth = 20
# wpercent = (basewidth/float(img.size[0]))
# hsize = int((float(img.size[1])*float(wpercent)))
# img = img.resize((basewidth,hsize), Image.ANTIALIAS)
# img.save(os.path.join(os.getcwd(), 'src/newUI/images/cell.png'))

WALK_RIGHT = [pygame.image.load(os.path.join(os.getcwd(), 'src/images/cell.png'))]
WALK_LEFT = [pygame.image.load(os.path.join(os.getcwd(), 'src/images/cell.png'))]
BG = pygame.image.load(os.path.join(os.getcwd(), 'src/images/water2.png'))
CHAR = pygame.image.load(os.path.join(os.getcwd(), 'src/images/cell.png'))
CLOCK = pygame.time.Clock()

class Cell(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.size = 20
        self.width = width
        self.height = height
        self.vel = 10
        self.direction = Step.UP

    def draw(self):
        WIN.blit(CHAR, (self.x, self.y))

    def check_collision(self, food):
        d = math.hypot(self.x - food.x, self.y - food.y)
        if d < self.size + food.size:
            print("EATEN! d=", d, " ", self.size, " + ", food.size)

    def move(self):

        dirs = []

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


def redrawGameWindow():
    WIN.blit(BG, (0, 0))
    food.draw(WIN)
    for i, _ in enumerate(cells):
        cells[i].draw()
    pygame.display.update()

cells=[]
for _ in range(C.INIT_NUM_CELLS):
    cells.append(Cell(500, 500, 20, 20))

BOARD = Board(50)
food = Food(100, 100)

#mainloop
run = True
while run:
    CLOCK.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    KEYS = pygame.key.get_pressed()
    for i in range(C.INIT_NUM_CELLS):
        cells[i].move()
        cells[i].check_collision(food)

    if KEYS[pygame.K_LEFT] and cells[0].x > 0:
        cells[0].x -= cells[0].vel
    if KEYS[pygame.K_RIGHT] and cells[0].x < C.BORDERS - cells[0].width:
        cells[0].x += cells[0].vel
    if KEYS[pygame.K_UP] and cells[0].y > 0:
        cells[0].y -= cells[0].vel
    if KEYS[pygame.K_DOWN] and cells[0].y < C.BORDERS - cells[0].height:
        cells[0].y += cells[0].vel
        
    redrawGameWindow()

pygame.quit()
