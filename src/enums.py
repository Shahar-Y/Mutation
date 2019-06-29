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