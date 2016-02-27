from __future__ import division
import random
from com.sirui.sim.config import Config

class Position(object):
    # Coordinate in a 2D plane
    LEFT = 0
    RIGHT = 1
    Front = 2
    Rear = 3
    def __init__(self, x = None, y = None, z = None, k = None):
        if x is None:
            self.x = random.randint(0, Config.SCOPE_SIZE-1)
        else:
            self.x = Position.edgeBound(x)
        if y is None:
            self.y = random.randint(0, Config.SCOPE_SIZE-1)
        else:
            self.y = Position.edgeBound(y)
        if z is None:
            self.z = None
        else:
            self.z = Position.heightBound(z)
        if k is None:
            self.k = 0
        else:
            self.k = k

    @classmethod
    def getLeftPosition(cls, position):
        return Position(position.x-1, position.y, position.z, position.k)
    @classmethod
    def getRightPosition(cls, position):
        return Position(position.x+1, position.y, position.z, position.k)
    @classmethod
    def getFrontPosition(cls, position):
        return Position(position.x, position.y-1, position.z, position.k)
    @classmethod
    def getRearPosition(cls, position):
        return Position(position.x, position.y+1, position.z, position.k)
    @classmethod
    def getUpPosition(cls, position):
        return Position(position.x, position.y, position.z+1, position.k)
    @classmethod
    def getDownPosition(cls, position):
        return Position(position.x, position.y, position.z-1, position.k)

    @classmethod
    def edgeBound(cls, i):
        # utility method to confine position with field boundary
        if i < 0:
            i += Config.SCOPE_SIZE
        i %= Config.SCOPE_SIZE
        return i

    @classmethod
    def heightBound(cls, i):
        # utility method to confine position with field boundary
        if i < 0:
            i = 0
        elif i >= Config.SCOPE_HEIGHT:
            i = Config.SCOPE_HEIGHT-1
        else:
            pass
        return i

    @classmethod
    def getNeighborPositions(cls, position):
        # return a list of all neighbor site positions in sequence
        # include underneath and above
        return [cls.getLeftPosition(position), cls.getRightPosition(position), cls.getFrontPosition(position), \
                cls.getRearPosition(position), cls.getUpPosition(position), cls.getDownPosition(position)]

    @classmethod
    def getSameHeightNeighborPositions(cls, position):
        # return a list of all neighbor site positions in sequence
        # include underneath and above
        return [cls.getLeftPosition(position), cls.getRightPosition(position), cls.getFrontPosition(position), \
                cls.getRearPosition(position)]

    def isNeighbor(self, other):
        if self.getLeftPosition(self) == other or  self.getRightPosition(self) == other or \
            self.getFrontPosition(self) == other or self.getRearPosition(self) == other:
            return True
        else:
            return False

    def toCoordinate(self):
        # change coordinate from lattice to 3D euclidean
        return (self.x, self.y, self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.k == other.k

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y, self.z, self.k))