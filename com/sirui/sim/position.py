from __future__ import division
import random
from com.sirui.sim import config
from com.sirui.sim.config import Config
from math import sqrt
class Position(object):

    ONE = 0
    TWO = 1
    THREE = 3

    def __init__(self, x = None, y = None, k = None):
        if x is None:
            self.x = random.randint(0, Config.SCOPE_SIZE-1)
        else:
            self.x = Position.edgeBound(x)
        if y is None:
            self.y = random.randint(0, Config.SCOPE_SIZE-1)
        else:
            self.y = Position.edgeBound(y)
        if k is None:
            self.k = random.randint(0, 1)
        else:
            self.k = k

    @classmethod
    def getNeighbor1Position(cls, position):
        if position.k == 0:
            return Position(position.x, position.y, 1)
        else:
            return Position(position.x, position.y, 0)

    @classmethod
    def getNeighbor2Position(cls, position):
        if position.k == 0:
            return Position(position.x-1, position.y, 1)
        else:
            return Position(position.x+1, position.y, 0)

    @classmethod
    def getNeighbor3Position(cls, position):
        if position.k == 0:
            return Position(position.x-1, position.y+1, 1)
        else:
            return Position(position.x+1, position.y-1, 0)

    @classmethod
    def edgeBound(cls, i):
        # utility method to confine position with field boundary
        if i < 0:
            i += Config.SCOPE_SIZE
        i %= Config.SCOPE_SIZE
        return i

    def toCoordinate(self):
        # change coordinate from lattice to 3D euclidean
        # [1, 1/2; 0, sqrt(3)/2]
        c0 = (self.x + 0.5 * self.y, self.y * sqrt(3) / 2)
        c1 = (1/2, -1/2/sqrt(3)) # relate to c[0]
        return (c0[0] + self.k * c1[0], c0[1] + self.k * c1[1], 0)

