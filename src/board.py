from typing import List
import random
from enums import TileType
import constants as C
from map_tile import MapTile

# Characters can move around and do cool stuff

def get_rand_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Character(MapTile):
    def __init__(self, name, health, col, row, size, hunger, sight, color):
        MapTile.__init__(self, name, col, row, TileType.Cell)
        self.health = health
        self.hunger = hunger
        self.sight = sight
        self.size = size
        self.is_dead = False
        self.color = color
        self.times_replicated = 0

    def food_eaten(self):
        self.health += 10
        if self.size < 10:
            self.size += 1
        if self.hunger - C.FOOD_WORTH >= 0:
            self.hunger = self.hunger - C.FOOD_WORTH
        else:
            self.hunger = 0
        BOARD.num_food -= 1
        if self.health >= C.REPRO_HEALTH:
            self.health = 0
            self.reproduce()


    def handle_step(self, col_advance, row_advance):
        new_col = self.col + col_advance
        new_row = self.row + row_advance
        curr_tile = BOARD.Grid[new_col][new_row]
        if curr_tile.type == TileType.Food:
            self.food_eaten()

        if curr_tile.type == TileType.Cell and curr_tile.size < self.size:
            print(self.col, ", ", self.row, " eating cell in ", new_col, ", ", new_row)
            curr_tile.is_dead = True
            self.food_eaten()
            print("done")

        if curr_tile.type == TileType.Grass or curr_tile.type == TileType.Food:
            BOARD.Grid[self.col][self.row] = MapTile(
                "Grass", self.col, self.row, TileType.Grass)
            self.col = new_col
            self.row = new_row
            BOARD.Grid[new_col][new_row] = self
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

    def choose_direction(self):
        if self.is_dead: 
            return True
        # search for food in sight
        for i in range(0, self.sight+1):
            array = get_close_array(i)
            random.shuffle(array)
            for index in array:
                if has_food(self, self.col + index[0], self.row + index[1]):
                    return self.move(get_directions(index[0], index[1]))

        # If the cell doesn't see food:
        num = random.randint(0, 3)
        return self.move(int_to_direction(num))

    # Checks if anything is on top of the grass in the direction that the character wants to move.
    # Used in the move function

    def collides(self, direction):
        if direction == "UP":
            if (BOARD.Grid[self.col][self.row-1]).type == TileType.Rock:
                return True
        elif direction == "LEFT":
            if (BOARD.Grid[self.col-1][self.row]).type == TileType.Rock:
                return True
        elif direction == "RIGHT":
            if (BOARD.Grid[self.col+1][self.row]).type == TileType.Rock:
                return True
        elif direction == "DOWN":
            if (BOARD.Grid[self.col][self.row+1]).type == TileType.Rock:
                return True
        return False

    def die(self):
        BOARD.Grid[self.col][self.row] = MapTile(
            "Grass", self.col, self.row, TileType.Grass)
        BOARD.num_cells -= 1
        del self

    def reproduce(self):
        col, row = self.adjasent_free_space()
        if col < 0:
            return
        new_size = 1 if int(self.size/2) == 0 else int(self.size/2)
        self.size = new_size
        if self.times_replicated > 5:
            self.color = get_rand_color()
            self.times_replicated = 0

        self.hunger = int(100-(100-self.hunger)/2)
        new_cell = Character("cell" + str(Map.index), 0,
                             col, row, new_size, self.hunger, C.DEFAULT_SIGHT, self.color)
        self.times_replicated += 1
        new_cell.times_replicated = self.times_replicated
        BOARD.Grid[col][row] = new_cell
        BOARD.index += 1
        BOARD.num_cells += 1

    def adjasent_free_space(self):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not(i == j and i == 0):
                    if BOARD.Grid[self.col + i][self.row + j].type == TileType.Grass:
                        return self.col + i, self.row + j
        return -1, -1


# The main class; where the action happens
class Map(object):
    index = 1
    num_food = 0
    num_cells = 0
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
    Hero = Character("Hero", 0, RandomColumn, RandomRow,
                     C.INIT_SIZE, C.INIT_HUNGER, C.DEFAULT_SIGHT, C.RED)
    num_cells += 1
    Grid[RandomColumn][RandomRow] = Hero

    def spread_food(self, num):
        for i in range(num):
            tries = 0
            while tries < 100:
                tries += 1
                rand_col = random.randint(0, C.MAP_SIZE - 1)
                rand_row = random.randint(0, C.MAP_SIZE - 1)
                if self.Grid[rand_col][rand_row].type == TileType.Grass:
                    temp_tile = MapTile(
                        "Food", rand_col, rand_row, TileType.Food)
                    self.Grid[rand_col][rand_row] = temp_tile
                    self.num_food += 1
                    break


def get_close_array(sight):
    array = []
    if sight == 0:
        return array
    for i in range(0, sight+1):
        col = i
        row = sight-i
        array.append([col, row])
        array.append([-col, -row])
        if col != 0 and row != 0:
            array.append([-col, row])
            array.append([col, -row])
    return array


def has_food(cell, col, row):
    if col >= 0 and col < C.MAP_SIZE and row >= 0 and row <= C.MAP_SIZE:
        if (BOARD.Grid[col][row].type == TileType.Food) or (BOARD.Grid[col][row].type == TileType.Food and cell.size - BOARD.Grid[col][row] >= C.EATING_SIZE):
            return True
    return False


def get_directions(col_step, row_step):
    if col_step < 0:
        return "LEFT"
    elif row_step < 0:
        return "UP"
    elif col_step > 0:
        return "RIGHT"
    elif row_step > 0:
        return "DOWN"
    return "DOWN"


def int_to_direction(num):
    if num % 4 == 0:
        return "LEFT"
    if num % 4 == 1:
        return "RIGHT"
    if num % 4 == 2:
        return "UP"
    if num % 4 == 3:
        return "DOWN"
    return "LEFT"


BOARD = Map()
