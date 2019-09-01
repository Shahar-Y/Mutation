# This is a pygame application and sample classes for
# the organization of a pygame application.
# source:https://kentdlee.github.io/SCSI/build/html/index.html

import pygame
import random
import os

SIZE = 800
# Notice here that Ball inherits from Sprite so it gets
# all the code associated with Sprites which is quite
# a bit.
class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y,dx=0,dy=0):
        print('******************')
        print(os.getcwd())
        super().__init__()
        self.image = pygame.image.load(os.path.join('src', 'succerball.gif'))
        self.rect = self.image.get_rect()
        self.originalImage = self.image
        self.rect.x = x
        self.rect.y = y
        self.dx = dx
        self.dy = dy

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y

    def move(self):
        if self.rect.x + self.dx > SIZE:
            print(self.rect.x, ', ', self.dx, ', ', self.rect.x+self.dx)
            self.dx = -self.dx
        if self.rect.y + self.dy > SIZE:
            self.dy = -self.dy
        if self.rect.y + self.dy < 0:
            self.dy = -self.dy
        if self.rect.x + self.dx < 0:
            print(self.rect.x, ', ', self.dx, ', ', self.rect.x+self.dx)
            self.dx = -self.dx
        self.rect.x += self.dx
        self.rect.y += self.dy

class App:
    def __init__(self):
        self.running = True
        self.screen = None
        self.size = self.width, self.height = SIZE, SIZE


    def on_init(self):
        # The following lines are needed for any pygame.
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.running = True

        # A surface is a solid colored box. In this case it is green.
        self.bgImg = pygame.Surface((SIZE,SIZE))
        self.bgImg.fill((100,255,130))
        # blit displays it on the screen (actually in the buffer).
        self.screen.blit(self.bgImg,(0,0))

        pygame.display.set_caption("Bouncing Balls")

        # self.sprites is a RenderUpdates group. A group is a group of sprites. Groups
        # provide the ability to draw sprites on the screen and other management of
        # sprites.
        self.sprites = pygame.sprite.RenderUpdates()

        # The ball is one of the sprites. The self.balls list is the list of balls
        # bouncing on the screen.
        for i in range(1):
            ball = Ball(random.uniform(10,590),random.uniform(10,590), \
               random.uniform(-2,2),random.uniform(-2,2))
            self.sprites.add(ball)

        return True


    def on_event(self, event):
        # This is an event processing function that is called with an event when it occurs.
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball = Ball(random.uniform(0,500),random.uniform(0,500), \
                   random.uniform(-6,6),random.uniform(-6,6))
                self.sprites.add(ball)
            if event.key == pygame.K_DOWN:
                self.sprites[0].dx -= 1

    def on_loop(self):
        # The on_loop is called below in the on_execute. This handles the changes
        # to the model of this program. It does not do any drawing.
        for ball in self.sprites:
            ball.move()

    def on_render(self):
        # The on_render is responsible for rendering or drawing the
        # frame.
        # These next lines clear each sprite from the screen by redrawing
        # the background behind that sprite.
        self.sprites.clear(self.screen,self.bgImg)

        # These next lines call blit to draw each sprite on the screen
        self.sprites.draw(self.screen)

        # Since double buffering is used, the flip method
        # switches the displayed buffer and the drawing buffer.
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if not self.on_init():
            self._running = False

        while(self.running):
            # The following get method call is a non-blocking
            # call that gets an event if one is ready. Otherwise
            # it drops through the for loop.
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()