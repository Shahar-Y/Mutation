# Code source: https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/optimization/
import pygame
import os
from PIL import Image
pygame.init()

BORDERS = 1000
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


class Cell(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[0], (self.x,self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[0], (self.x,self.y))
            self.walkCount +=1
        else:
            win.blit(char, (self.x,self.y))



def redrawGameWindow():
    win.blit(bg, (0,0))
    man.draw(win)
    
    pygame.display.update()


#mainloop
man = Cell(600, 500, 50,10)
run = True
while run:
    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.vel
        man.left = True
        man.right = False
    elif keys[pygame.K_RIGHT] and man.x < BORDERS - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
    else:
        man.right = False
        man.left = False
        man.walkCount = 0
        
    if not(man.isJump):
        if keys[pygame.K_SPACE]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
            
    redrawGameWindow()

pygame.quit()