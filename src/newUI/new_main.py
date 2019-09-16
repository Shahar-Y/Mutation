# Code source: https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/optimization/
import pygame
import os
from PIL import Image
from enums import Step, int_to_step
import random
from board import Board, Food

pygame.init()

BORDERS = 900
win = pygame.display.set_mode((BORDERS,BORDERS))
img = Image.open(os.path.join(os.getcwd(), 'src/images/cell.png'))
basewidth = 20
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)
img.save(os.path.join(os.getcwd(), 'src/newUI/images/cell.png'))

win = pygame.display.set_mode((BORDERS,BORDERS))
img = Image.open(os.path.join(os.getcwd(), 'src/images/algea2.png'))
basewidth = 20
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)
img.save(os.path.join(os.getcwd(), 'src/newUI/images/algea.png'))

walkRight = [pygame.image.load(os.path.join(os.getcwd(), 'src/images/cell.png'))]
walkLeft = [pygame.image.load(os.path.join(os.getcwd(), 'src/images/cell.png'))]
bg = pygame.image.load(os.path.join(os.getcwd(), 'src/images/water2.png'))
char = pygame.image.load(os.path.join(os.getcwd(), 'src/images/cell.png'))
clock = pygame.time.Clock()

class Cell(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 4
        self.walkCount = 0
        self.jumpCount = 10
        self.direction = Step.UP

    def draw(self, win):
        win.blit(char, (self.x,self.y))

    def move(self, board):

        if food.x < self.x:
            self.direction = Step.LEFT
        elif food.x > self.x:
            self.direction = Step.RIGHT
        elif food.y < self.y:
            self.direction = Step.UP
        elif food.y > self.y:
            self.direction = Step.DOWN

        change_dir = random.randint(0,5)
        if change_dir == 0:
            n = random.randint(0,3)
            self.direction = int_to_step(n)

        if self.direction == Step.LEFT and self.x > 0:
            self.x -= self.vel
        if self.direction == Step.RIGHT and self.x < BORDERS - self.width:
            self.x += self.vel
        if self.direction == Step.UP and self.y > 0:
            self.y -= self.vel
        if self.direction == Step.DOWN and self.y < BORDERS - self.height:
            self.y += self.vel


def redrawGameWindow():
    win.blit(bg, (0, 0))
    food.draw(win)
    for i, _ in enumerate(cells):
        cells[i].draw(win)
    pygame.display.update()

num_cells = 50
cells=[]
for _ in range(num_cells):
    cells.append(Cell(500,500,20,20))

board = Board(50)
food = Food(100, 100)

#mainloop
run = True
while run:
    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    for i in range(num_cells):
        cells[i].move([])

    if keys[pygame.K_LEFT] and cells[0].x > 0:
        cells[0].x -= cells[0].vel
    if keys[pygame.K_RIGHT] and cells[0].x < BORDERS - cells[0].width:
        cells[0].x += cells[0].vel
    if keys[pygame.K_UP] and cells[0].y > 0:
        cells[0].y -= cells[0].vel
    if keys[pygame.K_DOWN] and cells[0].y < BORDERS - cells[0].height:
        cells[0].y += cells[0].vel
            
    redrawGameWindow()

pygame.quit()