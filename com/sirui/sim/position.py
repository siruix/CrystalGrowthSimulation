import random
from com.sirui.sim import config
from com.sirui.sim.config import Config
class Position(object):
    # Coordinate in a 2D plane
    LEFT = 0
    RIGHT = 1
    UP = 3
    DOWN = 4
    def __init__(self, x = None, y = None):
        if x is None:
            self.x = random.randint(0, Config.SCOPE_SIZE-1)
        else:
            self.x = Position.edgeBound(x)
        if y is None:
            self.y = random.randint(0, Config.SCOPE_SIZE-1)
        else:
            self.y = Position.edgeBound(y)

    @classmethod
    def getLeftPosition(cls, position):
        return Position(position.x-1, position.y)
    @classmethod
    def getRightPosition(cls, position):
        return Position(position.x+1, position.y)
    @classmethod
    def getUpPosition(cls, position):
        return Position(position.x, position.y-1)
    @classmethod
    def getDownPosition(cls, position):
        return Position(position.x, position.y+1)

    @classmethod
    def edgeBound(cls, i):
        # utility method to confine position with field boundary
        if i < 0:
            i += Config.SCOPE_SIZE
        i %= Config.SCOPE_SIZE
        return i