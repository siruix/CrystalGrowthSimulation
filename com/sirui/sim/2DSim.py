from __future__ import print_function
import random
import simpy
from com.sirui.sim.monitor import Monitor

RANDOM_SEED = 42
SCOPE_SIZE = 5
NUM_ATOM = 3
SIM_TIME = 20     # Simulation time in minutes

class Field(object):
    def __init__(self, env, scope_size):
        self.env = env
        # one piece of resource for each location
        self.locations = [simpy.Resource(env) for i in range(scope_size)]

class Atom(object):
    def __init__(self, id, field, monitor, position=None):
        self.id = id
        self.field = field
        self.monitor = monitor
        if position is None:
            # generate initial position using collision avoidance
            while True:
                position = random.randint(0, SCOPE_SIZE-1)
                if self.field.locations[position].count == 0:
                    self.position = position
                    break
        else:
            self.position = position
        self.request = self.field.locations[self.position].request()
        self.next_positions = [-1, 1]
        # yield self.request
    def edgeBound(self, position):
        # utility method to confine position with location boundary
        if position < 0:
            position += SCOPE_SIZE
        position %= SCOPE_SIZE
        return position
    def getNextPosition(self):
        # next hop position should based on probability distribution
        rn = random.randint(0, 1)
        return self.edgeBound(self.position + self.next_positions[rn])

    def getHopInterval(self, num_neighbor):
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
    def getNumNeighbor(self):
        left_position = self.edgeBound(self.position-1)
        right_position = self.edgeBound(self.position+1)
        return self.field.locations[left_position].count + self.field.locations[right_position].count
    def run(self, env):
        yield self.request
        print("Atom %s at Location of %d" % (self.id, self.position))
        self.log()
        yield env.timeout(1)
        while True:
            num_neighbor = self.getNumNeighbor()
            hop_interval = self.getHopInterval(num_neighbor)
            if num_neighbor == 2:# inland atom never hop
                print("Atom %s at Location of %d not at edge. No move" % (self.id, self.position))
                yield env.timeout(1)
                continue

            yield env.timeout(hop_interval)
            print("Atom %s at Location of %d" % (self.id, self.position))
            # get next hopping position
            next_position = self.getNextPosition()
            # if next_position == self.position:
            #     print('%s hop to same location' % (self.id))
            #     continue
            # #
            if self.field.locations[next_position].count != 0:
                print("Collision! Atom %s tries to hop to Location %d but occupied. No move" % (self.id, next_position))
            else:
                self.field.locations[self.position].release(self.request)
                self.request = self.field.locations[next_position].request()
                yield self.request
                self.position = next_position
                print('Atom %s hops to Location of %d.' % (self.id, self.position))
                self.log()
    def log(self):
        self.monitor.data[env.now][self.id] = self.position
def setup(env, monitor, scope_size, num_atom):
    field = Field(env, scope_size)
    for i in range(num_atom):
        env.process(Atom(i, field, monitor).run(env))

    # Create more cars while the simulation is running
    # Create more atom as net deposition rate
    while True:
        yield env.timeout(1)
        print("clock: %d" % env.now)


# Setup and start the simulation
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
monitor = Monitor(SIM_TIME, NUM_ATOM)
env.process(setup(env, monitor, SCOPE_SIZE, NUM_ATOM))

# Execute!
env.run(until=SIM_TIME)
