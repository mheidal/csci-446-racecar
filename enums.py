from enum import IntEnum

class CrashType(IntEnum):
    RESTART = 0,
    STOP = 1

class CellType(IntEnum):
    WALL = 0
    START = 1
    FINISH = 2
    TRACK = 3


class TransitionType(IntEnum):
    CRASH = 0
    WIN = 1
    MOVE = 2