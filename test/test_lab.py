from enum import Enum


class State(Enum):
    IDLE = 1
    WALK = 2
    RUN = 3


print(State.IDLE)


class Color(Enum):
    BLACK = (0, 0, 0)


print(repr(Color.BLACK))