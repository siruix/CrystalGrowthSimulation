from __future__ import print_function
import random
import simpy
from enum import Enum
from com.sirui.sim.monitor import Monitor
from com.sirui.sim.resources import *

RANDOM_SEED = 42
SCOPE_SIZE = 3
NUM_ATOM = 3
SIM_TIME = 50     # Simulation time in sim clock

# TODO add evaporation rate
# TODO add two dimension
# TODO Use Logging instead of print

class Position(object):
    # Coordinate in a 2D plane
    LEFT = 0
    RIGHT = 1
    UP = 3
    DOWN = 4
    def __init__(self, x = None, y = None):
        if x is None:
            self.x = random.randint(0, SCOPE_SIZE-1)
        else:
            self.x = Position.edgeBound(x)
        if y is None:
            self.y = random.randint(0, SCOPE_SIZE-1)
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
            i += SCOPE_SIZE
        i %= SCOPE_SIZE
        return i

class Atom(object):
    def __init__(self, id, field, monitor, env, position=None):
        self.id = id
        self.field = field
        self.monitor = monitor
        self.env = env
        if position is None:
            # generate initial position using collision avoidance
            while True:
                position = Position()
                if self.field.getSite(position).resource.count == 0:
                    self.position = position
                    break
        else:
            self.position = position
        self.request = self.field.getSite(self.position).resource.request()
        self.process = self.env.process(self.run())

    def getUnoccupiedNeighborDirections(self):
        # return a list of possible move direction
        # Now it's for one dimension
        possible_next_direction_list = []
        if self.field.getSite(Position.getLeftPosition(self.position)).resource.count == 0:
            possible_next_direction_list.append(Position.LEFT)
        if self.field.getSite(Position.getRightPosition(self.position)).resource.count == 0:
            possible_next_direction_list.append(Position.RIGHT)
        if self.field.getSite(Position.getUpPosition(self.position)).resource.count == 0:
            possible_next_direction_list.append(Position.UP)
        if self.field.getSite(Position.getDownPosition(self.position)).resource.count == 0:
            possible_next_direction_list.append(Position.DOWN)
        return possible_next_direction_list

    def getNextPosition(self):
        # Hop to the a neighbor site which is not occupied
        possible_next_direction_list = self.getUnoccupiedNeighborDirections()
        # e.g. possible_next_direction_list = [Positions.LEFT, Positions.RIGHT]
        if len(possible_next_direction_list) == 0:
            return self.position
        rn = random.randint(0, len(possible_next_direction_list)-1)
        if possible_next_direction_list[rn] == Position.LEFT:
            next_position = Position.getLeftPosition(self.position)
        elif possible_next_direction_list[rn] == Position.RIGHT:
            next_position = Position.getRightPosition(self.position)
        elif possible_next_direction_list[rn] == Position.UP:
            next_position = Position.getUpPosition(self.position)
        elif possible_next_direction_list[rn] == Position.DOWN:
            next_position = Position.getDownPosition(self.position)
        else:
            next_position = self.position
            print("Exception: Invalid next position. ")
        return next_position

    def getNeighbors(self):
        # Define neighbor region. Here use 2D plane, which has four neighbors
        left_position = Position.getLeftPosition(self.position)
        right_position = Position.getRightPosition(self.position)
        up_position = Position.getUpPosition(self.position)
        down_position = Position.getDownPosition(self.position)
        neighbors = []
        if self.field.getSite(left_position).atom != None:
            neighbors.append(field.getSite(left_position).atom)
        if self.field.getSite(right_position).atom != None:
            neighbors.append(field.getSite(right_position).atom)
        if self.field.getSite(up_position).atom != None:
            neighbors.append(field.getSite(up_position).atom)
        if self.field.getSite(down_position).atom != None:
            neighbors.append(field.getSite(down_position).atom)
        return neighbors

    @staticmethod
    def getHopInterval(num_neighbor):
        # Probability model that determines hop timeout
        # TODO change to probability model using arrhenius equation
        hop_interval = 1000
        if num_neighbor == 0:
            hop_interval = 1
        elif num_neighbor == 1:
            hop_interval = 4
        elif num_neighbor == 2:
            hop_interval = 16
        elif num_neighbor == 3:
            hop_interval = 64
        elif num_neighbor == 4:
            hop_interval = 256
        else:
            print('Exception: Invalid hop interval')
        return hop_interval

    def updateNeighborTimeout(self):
        neighbors = self.getNeighbors()
        for neighbor in neighbors:
            num_neighbor = len(neighbor.getNeighbors())
            hop_interval = Atom.getHopInterval(num_neighbor)
            print("Atom %s at Site (%d, %d) request interrupt with timeout %d" % (neighbor.id, neighbor.position.x, neighbor.position.y, hop_interval))
            neighbor.process.interrupt(hop_interval)

    def run(self):
        yield self.request
        site = self.field.getSite(self.position)
        site.atom = self
        # self.neighbors = 0 # default
        print("Atom %s at Site (%d, %d)" % (self.id, self.position.x, self.position.y))
        self.log()
        # init all atoms
        yield self.env.timeout(1)
        while True:
            hop_interval = Atom.getHopInterval(len(self.getNeighbors()))
            if len(self.getNeighbors()) == 4:# inland atom never hop
                print("Atom %s at Site (%d, %d) not at edge. No move" % (self.id, self.position.x, self.position.y))
                yield self.env.timeout(1)
                continue

            while True:
                try:
                    print("Atom %s at Site (%d, %d) wait timeout %d" % (self.id, self.position.x, self.position.y, hop_interval))
                    yield self.env.timeout(hop_interval)
                    print("Atom %s at Site (%d, %d) resume" % (self.id, self.position.x, self.position.y))
                    break
                except simpy.Interrupt as i:
                    print("Atom %s at Site (%d, %d) timeout reset to %d" % (self.id, self.position.x, self.position.y, i.cause))
                    hop_interval = i.cause
                except:
                    print("Unexpected Exception: Atom %s at Site (%d, %d)" % (self.id, self.position.x, self.position.y))

            # get next hopping position
            next_position = self.getNextPosition()

            if self.field.getSite(next_position).resource.count != 0:
                print("Collision! Atom %s tries to hop to Site %d but occupied. No move" % (self.id, next_position))
            else:
                self.field.getSite(self.position).resource.release(self.request)
                self.field.getSite(self.position).atom = None
                # Update previous neighbors time out
                self.updateNeighborTimeout()
                print('Atom %s updates old neighbors.' % (self.id))

                self.request = self.field.getSite(next_position).resource.request()
                print('Atom %s requests to Site (%d, %d).' % (self.id, next_position.x, next_position.y))
                yield self.request
                print('Atom %s granted Site (%d, %d).' % (self.id, next_position.x, next_position.y))

                site = self.field.getSite(next_position)
                site.atom = self
                self.position = next_position

                # Update new neighbors timeout.
                self.updateNeighborTimeout()
                print('Atom %s updates new neighbors.' % (self.id))
                self.log()

    def log(self):
        # log current status into monitor
        self.monitor.data[self.env.now][self.id] = self.position

def clock(env, monitor):
    while True:
        yield env.timeout(1)
        print("clock: %d" % env.now)

if __name__ == '__main__':
    # Setup and start the simulation
    random.seed(RANDOM_SEED)  # This helps reproducing the results

    # Create an environment and start the setup process
    env = simpy.Environment()
    monitor = Monitor(SIM_TIME, NUM_ATOM)
    field = Field(env, SCOPE_SIZE)
    atoms = [Atom(i, field, monitor, env) for i in range(NUM_ATOM)]
    env.process(clock(env, monitor))
    # Execute!
    env.run(until=SIM_TIME)
