# Code source: https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/optimization/
import random
import os
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
        self.width = width
        self.height = height
        self.vel = 4
        self.direction = Step.UP

    def draw(self):
        WIN.blit(CHAR, (self.x, self.y))

    def move(self):

        if food.x < self.x:
            self.direction = Step.LEFT
        elif food.x > self.x:
            self.direction = Step.RIGHT
        elif food.y < self.y:
            self.direction = Step.UP
        elif food.y > self.y:
            self.direction = Step.DOWN

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
