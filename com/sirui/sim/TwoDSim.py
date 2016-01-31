from __future__ import print_function
import random
import logging
import os
from com.sirui.sim.monitor import Monitor
from com.sirui.sim.resources import *
from com.sirui.sim import config
from com.sirui.sim.position import Position

# TODO add evaporation rate
# TODO monitor unnecessary



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
            logger.error("Invalid next position. ")
        return next_position

    def getNeighbors(self):
        # Define neighbor region. Here use 2D plane, which has four neighbors
        left_position = Position.getLeftPosition(self.position)
        right_position = Position.getRightPosition(self.position)
        up_position = Position.getUpPosition(self.position)
        down_position = Position.getDownPosition(self.position)
        neighbors = []
        if self.field.getSite(left_position).atom != None:
            neighbors.append(self.field.getSite(left_position).atom)
        if self.field.getSite(right_position).atom != None:
            neighbors.append(self.field.getSite(right_position).atom)
        if self.field.getSite(up_position).atom != None:
            neighbors.append(self.field.getSite(up_position).atom)
        if self.field.getSite(down_position).atom != None:
            neighbors.append(self.field.getSite(down_position).atom)
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
            logger.error('Invalid hop interval. ')
        return hop_interval

    def updateNeighborTimeout(self):
        neighbors = self.getNeighbors()
        for neighbor in neighbors:
            num_neighbor = len(neighbor.getNeighbors())
            hop_interval = Atom.getHopInterval(num_neighbor)
            logger.debug("Atom %s at Site (%d,%d) request interrupt with timeout %d. " % (neighbor.id, neighbor.position.x, neighbor.position.y, hop_interval))
            neighbor.process.interrupt(hop_interval)

    def run(self):
        yield self.request
        site = self.field.getSite(self.position)
        site.atom = self
        # self.neighbors = 0 # default
        logger.info("Clock %d Atom %s at Site (%d,%d). " % (self.env.now, self.id, self.position.x, self.position.y))
        self.log()
        # init all atoms
        yield self.env.timeout(1)
        while True:
            hop_interval = Atom.getHopInterval(len(self.getNeighbors()))
            # if len(self.getNeighbors()) == 4:# inland atom never hop
            #     logger.debug("Atom %s at Site (%d,%d) not at edge. No move. " % (self.id, self.position.x, self.position.y))
            #     yield self.env.timeout(1)
            #     continue

            while True:
                try:
                    logger.debug("Atom %s at Site (%d,%d) wait timeout %d. " % (self.id, self.position.x, self.position.y, hop_interval))
                    yield self.env.timeout(hop_interval)
                    logger.debug("Atom %s at Site (%d,%d) resume. " % (self.id, self.position.x, self.position.y))
                    break
                except simpy.Interrupt as i:
                    logger.debug("Atom %s at Site (%d,%d) timeout reset to %d. " % (self.id, self.position.x, self.position.y, i.cause))
                    hop_interval = i.cause
                except Exception, e:
                    logger.error("Atom %s at Site (%d,%d) interrupted. " % (self.id, self.position.x, self.position.y), exc_info=True)
                    raise(e)

            # get next hopping position
            next_position = self.getNextPosition()

            if self.field.getSite(next_position).resource.count != 0:
                if self.position == next_position:
                    logger.debug("Atom %s stays at Site (%d,%d). " % (self.id, next_position.x, next_position.y))
                else:
                    logger.warning("Collision! Atom %s tries to hop to Site (%d,%d) but occupied. No move. " % (self.id, next_position.x, next_position.y))

            else:
                self.field.getSite(self.position).resource.release(self.request)
                self.field.getSite(self.position).atom = None
                # Update previous neighbors time out
                self.updateNeighborTimeout()
                logger.debug('Atom %s updates old neighbors.' % (self.id))

                self.request = self.field.getSite(next_position).resource.request()
                logger.debug('Atom %s requests to Site (%d,%d).' % (self.id, next_position.x, next_position.y))
                try:
                    yield self.request
                except Exception, e:
                    logger.error("Atom %s at Site (%d,%d) interrupted. " % (self.id, self.position.x, self.position.y), exc_info=True)
                    raise(e)

                logger.debug('Atom %s granted Site (%d,%d).' % (self.id, next_position.x, next_position.y))
                logger.info('Clock %d Atom %s at Site (%d,%d).' % (self.env.now, self.id, next_position.x, next_position.y))
                site = self.field.getSite(next_position)
                site.atom = self
                self.position = next_position

                # Update new neighbors timeout.
                self.updateNeighborTimeout()
                # print('Atom %s updates new neighbors.' % (self.id))
                logger.debug('Atom %s updates new neighbors.' % (self.id))
                self.log()

    def log(self):
        # log current status into monitor
        self.monitor.data[self.env.now][self.id] = self.position

def clock(env, monitor):
    while True:
        yield env.timeout(1)
        logger.debug("clock: %d" % env.now)

def main():
    logger.info("Simulation starts. #Atom: %d, Field: %d*%d, Time: %d" % (config.NUM_ATOM, config.SCOPE_SIZE, config.SCOPE_SIZE, config.SIM_TIME))
    if config.SCOPE_SIZE * config.SCOPE_SIZE < config.NUM_ATOM:
        raise ValueError("Number of atom is too much")
    # Setup and start the simulation
    random.seed(config.RANDOM_SEED)  # This helps reproducing the results
    # Create an environment and start the setup process
    env = simpy.Environment()
    monitor = Monitor(config.SIM_TIME, config.NUM_ATOM)

    field = Field(env, config.SCOPE_SIZE)
    atoms = [Atom(i, field, monitor, env) for i in range(config.NUM_ATOM)]
    env.process(clock(env, monitor))
    # Execute!
    env.run(until=config.SIM_TIME)

if __name__ == '__main__':
    if os.path.exists('info.log'):
        os.remove('info.log')
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)
    logging.basicConfig(level=logging.DEBUG)

    # create a file handler
    handler = logging.FileHandler('info.log')
    handler.setLevel(logging.INFO)

    # create a logging format
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    main()