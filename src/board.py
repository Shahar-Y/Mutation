from typing import List
import random
from enums import TileType
import constants as C
from map_tile import MapTile

# Characters can move around and do cool stuff
class Character(object):
    def __init__(self, name, hp, col, row):
        self.name = name
        self.health = hp
        self.col = col
        self.row = row
        self.hunger = C.INIT_HUNGER

    def handle_step(self, col_advance, row_advance):
        new_col = self.col + col_advance
        new_row = self.row + row_advance
        curr_tile = Map.Grid[new_col][new_row]
        if curr_tile.type == TileType.Food:
            self.health += 10
            if self.hunger - C.FOOD_WORTH >= 0:
                self.hunger = self.hunger - C.FOOD_WORTH
            else:
                self.hunger = 0
            Map.num_food -= 1
            if self.health >= C.REPRO_HEALTH:
                self.health = 0
                self.reproduce()

        if curr_tile.type == TileType.Grass or curr_tile.type == TileType.Food:
            Map.Grid[self.col][self.row] = MapTile("Grass", self.col, self.row, TileType.Grass)
            self.col = new_col
            self.row = new_row
            Map.Grid[new_col][new_row] = MapTile(self.name, new_col, new_row, TileType.Cell)
        self.hunger += 1
        if(self.hunger) >= 100:
            return True
        return False

    # This function is how a character moves around in a certain direction
    def move(self, direction):
        is_dead = False
        if direction == "UP":
            if self.row > 0 and not self.collides("UP"):
                is_dead = self.handle_step(0, -1)

        elif direction == "LEFT":
            if self.col > 0 and not self.collides("LEFT"):
                is_dead = self.handle_step(-1, 0)

        elif direction == "RIGHT":
            if self.col < C.MAP_SIZE-1 and not self.collides("RIGHT"):
                is_dead = self.handle_step(1, 0)

        elif direction == "DOWN":
            if self.row < C.MAP_SIZE-1 and not self.collides("DOWN"):
                is_dead = self.handle_step(0, 1)
        return is_dead

    # Checks if anything is on top of the grass in the direction that the character wants to move.
    # Used in the move function
    def collides(self, direction):
        if direction == "UP":
            if (Map.Grid[self.col][self.row-1]).type == TileType.Rock:
                return True
        elif direction == "LEFT":
            if (Map.Grid[self.col-1][self.row]).type == TileType.Rock:
                return True
        elif direction == "RIGHT":
            if (Map.Grid[self.col+1][self.row]).type == TileType.Rock:
                return True
        elif direction == "DOWN":
            if (Map.Grid[self.col][self.row+1]).type == TileType.Rock:
                return True
        return False

    def die(self):
        print('DYING :(')
        Map.Grid[self.col][self.row] = MapTile("Grass", self.col, self.row, TileType.Grass)
        Map.Cells.remove(self)
        del self

    def reproduce(self):
        col, row = self.adjasent_free_space()
        if col < 0:
            return
        print("reproducing!")
        new_cell = Character("Hero", 0, col, row)
        Map.Grid[col][row] = MapTile("cell" + str(Map.index), col, row, TileType.Cell)
        Map.index += 1
        Map.Cells.append(new_cell)

    def adjasent_free_space(self):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not(i == j and i == 0):
                    if Map.Grid[self.col + i][self.row + j].type == TileType.Grass:
                        return self.col + i, self.row + j
        return -1, -1


# The main class; where the action happens
class Map(object):
    index = 1
    num_food = 0
    Grid: List[List[MapTile]] = []*(C.MAP_SIZE*C.MAP_SIZE)

    empty_tile = MapTile("", 0, 0, TileType.Pixel)
    for row in range(C.MAP_SIZE*C.MAP_SIZE):     # Creating grid
        Grid.append([empty_tile])
        for Column in range(C.MAP_SIZE):
            Grid[row].append(empty_tile)

    for row in range(C.MAP_SIZE):     # Filling grid with grass
        for Column in range(C.MAP_SIZE):
            TempTile = MapTile("Grass", Column, row, TileType.Grass)
            Grid[Column][row] = TempTile

    RandomColumn = random.randint(0, C.MAP_SIZE - 1)
    RandomRow = random.randint(0, C.MAP_SIZE - 1)
    Hero = Character("Hero", 0, RandomColumn, RandomRow)
    Cells: List[Character] = [Hero]
    Grid[RandomColumn][RandomRow] = MapTile("Hero", RandomColumn, RandomRow, TileType.Cell)

    def spread_food(self, num):
        for i in range(num):
            tries = 0
            while tries < 100:
                tries += 1
                rand_col = random.randint(0, C.MAP_SIZE - 1)
                rand_row = random.randint(0, C.MAP_SIZE - 1)
                if self.Grid[rand_col][rand_row].type == TileType.Grass:
                    temp_tile = MapTile("Food", rand_col, rand_row, TileType.Food)
                    self.Grid[rand_col][rand_row] = temp_tile
                    self.num_food += 1
                    break