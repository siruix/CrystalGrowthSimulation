from __future__ import print_function
import random
import simpy
from com.sirui.sim.monitor import Monitor
from com.sirui.sim.resources import *
RANDOM_SEED = 42
SCOPE_SIZE = 5
NUM_ATOM = 3
SIM_TIME = 20     # Simulation time in minutes

# TODO add evaporation rate

class Atom(object):
    def __init__(self, id, field, monitor, env, position=None):
        self.id = id
        self.field = field
        self.monitor = monitor
        self.env = env
        if position is None:
            # generate initial position using collision avoidance
            while True:
                position = random.randint(0, SCOPE_SIZE-1)
                if self.field.locations[position].resource.count == 0:
                    self.position = position
                    break
        else:
            self.position = position
        self.request = self.field.locations[self.position].resource.request()
        # self.next_positions = [-1, 1]
        self.process = self.env.process(self.run())
        # yield self.request



    @classmethod
    def edgeBound(self, position):
        # utility method to confine position with location boundary
        if position < 0:
            position += SCOPE_SIZE
        position %= SCOPE_SIZE
        return position

    def getUnoccupiedNeighborLocations(self):
        # return a list of possible move direction
        # Now it's for one dimension
        possible_next_direction_list = []
        if self.field.locations[self.edgeBound(self.position-1)].resource.count == 0:
            possible_next_direction_list.append(-1)
        if self.field.locations[self.edgeBound(self.position+1)].resource.count == 0:
            possible_next_direction_list.append(1)
        return possible_next_direction_list

    def getNextPosition(self):
        # Hop to the a neighbor site which is not occupied
        possible_next_direction_list = self.getUnoccupiedNeighborLocations()
        # e.g. possible_next_direction_list = [-1, 1]
        if len(possible_next_direction_list) == 0:
            return self.position
        rn = random.randint(0, len(possible_next_direction_list)-1)
        return self.edgeBound(self.position + possible_next_direction_list[rn])

    @classmethod
    def getLeftPosition(cls, position):
        return cls.edgeBound(position-1)

    @classmethod
    def getRightPosition(cls, position):
        return cls.edgeBound(position+1)

    def getNeighbors(self):
        # Define neighbor region. Here use one dimensional neighbor, that has two neighbors
        left_position = self.getLeftPosition(self.position)
        right_position = self.getRightPosition(self.position)
        neighbors = []
        if self.field.locations[left_position].atom != None:
            neighbors.append(field.locations[left_position].atom)
        if self.field.locations[right_position].atom != None:
            neighbors.append(field.locations[right_position].atom)
        return neighbors

    @staticmethod
    def getHopInterval(num_neighbor):
        # Probability model that determines hop timeout
        # TODO change to probability model using arrhenius equation
        hop_interval = 100
        if num_neighbor == 0:
            hop_interval = 1
        elif num_neighbor == 1:
            hop_interval = 4
        elif num_neighbor == 2:
            hop_interval = 16
        else:
            pass
        return hop_interval

    def updateNeighborTimeout(self):
        neighbors = self.getNeighbors()
        for neighbor in neighbors:
            num_neighbor = len(neighbor.getNeighbors())
            hop_interval = Atom.getHopInterval(num_neighbor)
            print("Atom %s at Location of %d request interrupt with timeout %d" % (neighbor.id, neighbor.position, hop_interval))
            neighbor.process.interrupt(hop_interval)

    def run(self):
        yield self.request
        location = self.field.locations[self.position]
        location.atom = self
        # self.neighbors = 0 # default
        print("Atom %s at Location of %d" % (self.id, self.position))
        self.log()
        # init all atoms
        yield self.env.timeout(1)
        while True:
            hop_interval = Atom.getHopInterval(len(self.getNeighbors()))
            if len(self.getNeighbors()) == 2:# inland atom never hop
                print("Atom %s at Location of %d not at edge. No move" % (self.id, self.position))
                yield self.env.timeout(1)
                continue

            while True:
                try:
                    print("Atom %s at Location of %d wait timeout %d" % (self.id, self.position, hop_interval))
                    yield self.env.timeout(hop_interval)
                    print("Atom %s at Location of %d resume" % (self.id, self.position))
                    break
                except simpy.Interrupt as i:
                    print("Atom %s at Location of %d timeout reset to %d" % (self.id, self.position, i.cause))
                    hop_interval = i.cause
                except:
                    print("Unexpected Exception: Atom %s at Location of %d" % (self.id, self.position))

            # get next hopping position
            next_position = self.getNextPosition()

            if self.field.locations[next_position].resource.count != 0:
                print("Collision! Atom %s tries to hop to Location %d but occupied. No move" % (self.id, next_position))
            else:
                self.field.locations[self.position].resource.release(self.request)
                self.field.locations[self.position].atom = None
                # Update previous neighbors time out
                self.updateNeighborTimeout()
                print('Atom %s updates old neighbors.' % (self.id))

                self.request = self.field.locations[next_position].resource.request()
                print('Atom %s requests to Location %d.' % (self.id, next_position))
                yield self.request
                print('Atom %s granted Location %d.' % (self.id, next_position))

                location = self.field.locations[next_position]
                location.atom = self
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
