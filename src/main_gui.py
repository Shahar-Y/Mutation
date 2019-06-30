import random as random
import pygame as pygame
from enums import TileType
import time

pygame.init()                                 # start up dat pygame
clock = pygame.time.Clock()                   # for frame-rate or something? still not very sure
Screen = pygame.display.set_mode([1000, 1000])  # making the window
Done = False                                  # variable to keep track if window is open
MapSize = 25                                  # how many tiles in either direction of grid

TileWidth = 20                                # pixel sizes for grid squares
TileHeight = 20
TileMargin = 4

BLACK = (0, 0, 0)                             # some color definitions
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# The main class for stationary things that inhabit the grid ... grass, trees, rocks and stuff.
class MapTile(object):
    def __init__(self, name, column, row, type):
        self.type = type
        self.Name = name
        self.Column = column
        self.Row = row


# Characters can move around and do cool stuff
class Character(object):
    def __init__(self, name, hp, column, row):
        self.Name = name
        self.HP = hp
        self.Column = column
        self.Row = row

    def handle_step(self, col_advance, row_advance):
        new_col = self.Column + col_advance
        new_row = self.Row + row_advance
        if Map.Grid[new_col][new_row].type == TileType.Food:
            self.HP += 10
            print("new HP: {}".format(self.HP))
        if Map.Grid[new_col][new_row].type == TileType.Grass or Map.Grid[new_col][new_row].type == TileType.Food:
            Map.Grid[self.Column][self.Row] = MapTile("Grass", self.Column, self.Row, TileType.Grass)
            self.Row += row_advance
            self.Column += col_advance
            Map.Grid[self.Column][self.Row] = MapTile(self.Name, self.Column, self.Row, TileType.Cell)

    # This function is how a character moves around in a certain direction
    def Move(self, Direction):

        if Direction == "UP":
            if self.Row > 0 and (self.CollisionCheck("UP") is False):
                self.handle_step(0, -1)

        elif Direction == "LEFT":
            if self.Column > 0:
                if self.CollisionCheck("LEFT") == False:
                    self.handle_step(-1, 0)


        elif Direction == "RIGHT":
            if self.Column < MapSize-1:
                if self.CollisionCheck("RIGHT") == False:
                    self.handle_step(1, 0)

        elif Direction == "DOWN":
            if self.Row < MapSize-1:
                if self.CollisionCheck("DOWN") == False:
                    self.handle_step(0, 1)

    # Checks if anything is on top of the grass in the direction that the character wants to move.
    # Used in the move function
    def CollisionCheck(self, Direction):
        if Direction == "UP":
            if (Map.Grid[self.Column][(self.Row)-1]).type == TileType.Rock:
                return True
        elif Direction == "LEFT":
            if (Map.Grid[self.Column-1][(self.Row)]).type == TileType.Rock:
                return True
        elif Direction == "RIGHT":
            if (Map.Grid[self.Column+1][(self.Row)]).type == TileType.Rock:
                return True
        elif Direction == "DOWN":
            if (Map.Grid[self.Column][(self.Row)+1]).type == TileType.Rock:
                return True
        return False

    def Location(self):
        print("Coordinates: " + str(self.Column) + ", " + str(self.Row))

# The main class; where the action happens
class Map(object):
    global MapSize

    Grid = []

    for Row in range(MapSize):     # Creating grid
        Grid.append([])
        for Column in range(MapSize):
            Grid[Row].append([])

    for Row in range(MapSize):     # Filling grid with grass
        for Column in range(MapSize):
            TempTile = MapTile("Grass", Column, Row, TileType.Grass)
            Grid[Column][Row] = TempTile

    RandomColumn = random.randint(0, MapSize - 1)
    RandomRow = random.randint(0, MapSize - 1)
    Hero = Character("Hero", 10, RandomColumn, RandomRow)
    Grid[RandomColumn][RandomRow] = MapTile("Hero", RandomColumn, RandomRow, TileType.Cell)

    def SpreadFood(self, num):
        for i in range(num):
            RandomColumn = random.randint(0, MapSize - 1)
            RandomRow = random.randint(0, MapSize - 1)
            TempTile = MapTile("Food", RandomColumn, RandomRow, TileType.Food)
            self.Grid[RandomColumn][RandomRow] = TempTile


Map = Map()
Map.SpreadFood(60)


def int_to_direction(num):
    if num % 4 == 0:
        return "LEFT"
    if num % 4 == 1:
        return "RIGHT"
    if num % 4 == 2:
        return "UP"
    if num % 4 == 3:
        return "DOWN"


def run_game():
    done = False
    while not done:     # Main pygame loop
        time.sleep(0.1)
        num = random.randint(0, 3)
        Map.Hero.Move(int_to_direction(num))

        for event in pygame.event.get():         # catching events
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                Pos = pygame.mouse.get_pos()
                Column = Pos[0] // (TileWidth + TileMargin)  #Translating the position of the mouse into rows and columns
                Row = Pos[1] // (TileHeight + TileMargin)
                print(str(Row) + ", " + str(Column))

                # for i in range(len(Map.Grid[Column][Row])):
                #     print(str(Map.Grid[Column][Row][i].Name))  #print stuff that inhabits that square

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Map.Hero.Move("LEFT")
                if event.key == pygame.K_RIGHT:
                    Map.Hero.Move("RIGHT")
                if event.key == pygame.K_UP:
                    Map.Hero.Move("UP")
                if event.key == pygame.K_DOWN:
                    Map.Hero.Move("DOWN")

        Screen.fill(BLACK)

        for Row in range(MapSize):           # Drawing grid
            for Column in range(MapSize):
                if Map.Grid[Column][Row].type == TileType.Grass:
                    Color = WHITE
                if Map.Grid[Column][Row].type == TileType.Cell:
                    Color = BLUE
                if Map.Grid[Column][Row].type == TileType.Food:
                    Color = RED


                pygame.draw.rect(Screen, Color, [(TileMargin + TileWidth) * Column + TileMargin,
                                                 (TileMargin + TileHeight) * Row + TileMargin,
                                                 TileWidth,
                                                 TileHeight])

        clock.tick(60)      #Limit to 60 fps or something

        pygame.display.flip()     #Honestly not sure what this does, but it breaks if I remove it

run_game()

pygame.quit()

