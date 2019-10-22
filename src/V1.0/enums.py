from enum import Enum, auto


class TileType(Enum):
    Grass = auto()
    Pixel = auto()
    Cell = auto()
    Food = auto()
    Rock = auto()
    Antibiotics = auto()


class Step(Enum):
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    UP = "UP"
    DOWN = "DOWN"


class CFeatures:
    SPEED = auto()
    SIGHT = auto()
    REPLICATION = auto()
    FOOD = auto()
    MU_RATE = auto()
    HEALTH = auto()


def int_to_step(n):
    if n == 0:
        return Step.RIGHT
    elif n == 1:
        return Step.LEFT
    elif n == 2:       
        return Step.UP
    elif n == 3:
        return Step.DOWN
