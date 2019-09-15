# Code source: https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/optimization/
import pygame
import os
from PIL import Image
from enums import Step, int_to_step
import random

pygame.init()

BORDERS = 900
win = pygame.display.set_mode((BORDERS,BORDERS))
img = Image.open(os.path.join(os.getcwd(), 'src/images/cell.png'))
basewidth = 60
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)
img.save(os.path.join(os.getcwd(), 'src/images/cell.png')) 


walkRight = [pygame.image.load(os.path.join(os.getcwd(), 'src/images/cell.png'))]
walkLeft = [pygame.image.load(os.path.join(os.getcwd(), 'src/images/cell.png'))]
bg = pygame.image.load(os.path.join(os.getcwd(), 'src/images/water2.png'))
char = pygame.image.load(os.path.join(os.getcwd(), 'src/images/cell.png'))
clock = pygame.time.Clock()

rect1 = pygame.Rect(0,0,10,10)
rect2 = pygame.Rect(9,9,10,10)
print(str(rect1.colliderect(rect2)))

class Cell(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.walkCount = 0
        self.jumpCount = 10
        self.last_step = Step.UP

    def draw(self, win):
        win.blit(char, (self.x,self.y))

    def move(self, board):
        change_dir = random.randint(0,10)
        if change_dir == 0:
            n = random.randint(0,3)
            self.last_step = int_to_step(n)

        if self.last_step == Step.LEFT and cell.x > 0:
            cell.x -= cell.vel
        if self.last_step == Step.RIGHT and cell.x < BORDERS - cell.width:
            cell.x += cell.vel
        if self.last_step == Step.UP and cell.y > 0:
            cell.y -= cell.vel
        if self.last_step == Step.DOWN and cell.y < BORDERS - cell.height:
            cell.y += cell.vel
        





def redrawGameWindow():
    win.blit(bg, (0,0))
    cell.draw(win)
    
    pygame.display.update()


#mainloop
cell = Cell(600, 500, 60,60)
run = True
while run:
    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    cell.move([])

    if keys[pygame.K_LEFT] and cell.x > 0:
        cell.x -= cell.vel
    if keys[pygame.K_RIGHT] and cell.x < BORDERS - cell.width:
        cell.x += cell.vel
    if keys[pygame.K_UP] and cell.y > 0:
        cell.y -= cell.vel
    if keys[pygame.K_DOWN] and cell.y < BORDERS - cell.height:
        cell.y += cell.vel
            
    redrawGameWindow()

pygame.quit()