from __future__ import print_function
import random
import logging
import os
import datetime
from com.sirui.sim.resources import *
from com.sirui.sim.config import Config
from com.sirui.sim.position import Position

class Atom(object):
    id = 0 # keep track latest id
    def __init__(self, id, field, env, position):
        self.id = id
        self.field = field
        self.env = env
        self.position = position
        self.request = self.field.getSite(self.position).resource.request()
        self.process = self.env.process(self.run())
        site = self.field.getSite(self.position)
        site.atom = None

    @classmethod
    def createAtom(cls, field, env):
        # atom will not create if site occupied
        position = Position()
        if field.getSite(position).resource.count == 0:
            cls(Atom.id, field, env, position)
            Atom.id += 1

    @classmethod
    def createInitAtoms(cls, field, env, num_atom):
        # create all init atom in a batch
        Atom.id = 0
        while Atom.id < num_atom:
            # TODO improve efficiency
            # Must create atom
            while True:
                position = Position()
                if field.getSite(position).resource.count == 0:
                    cls(Atom.id, field, env, position)
                    Atom.id += 1
                    break


    def getUnoccupiedNeighborDirections(self):
        # return a list of possible move direction
        # Now it's for one dimension
        possible_next_direction_list = []
        if self.field.getSite(Position.getNeighbor1Position(self.position)).resource.count == 0:
            possible_next_direction_list.append(Position.ONE)
        if self.field.getSite(Position.getNeighbor2Position(self.position)).resource.count == 0:
            possible_next_direction_list.append(Position.TWO)
        if self.field.getSite(Position.getNeighbor3Position(self.position)).resource.count == 0:
            possible_next_direction_list.append(Position.THREE)

        return possible_next_direction_list

    def getNextPosition(self):
        # Hop to the a neighbor site which is not occupied
        possible_next_direction_list = self.getUnoccupiedNeighborDirections()
        if len(possible_next_direction_list) == 0:
            return self.position
        rn = random.randint(0, len(possible_next_direction_list)-1)
        if possible_next_direction_list[rn] == Position.ONE:
            next_position = Position.getNeighbor1Position(self.position)
        elif possible_next_direction_list[rn] == Position.TWO:
            next_position = Position.getNeighbor2Position(self.position)
        elif possible_next_direction_list[rn] == Position.THREE:
            next_position = Position.getNeighbor3Position(self.position)
        else:
            next_position = self.position
            logger = logging.getLogger(__name__)
            logger.error("Invalid next position. ")
        return next_position

    def getNeighbors(self):
        # Define neighbor region. Here assume graphene 2D plane, which has up to 3 neighbors
        # TODO depends on site of lattice, position1 will be different
        position1 = Position.getNeighbor1Position(self.position)
        position2 = Position.getNeighbor2Position(self.position)
        position3 = Position.getNeighbor3Position(self.position)

        neighbors = []
        if self.field.getSite(position1).atom != None:
            neighbors.append(self.field.getSite(position1).atom)
        if self.field.getSite(position2).atom != None:
            neighbors.append(self.field.getSite(position2).atom)
        if self.field.getSite(position3).atom != None:
            neighbors.append(self.field.getSite(position3).atom)

        return neighbors

    @staticmethod
    def getHopInterval(num_neighbor):
        # Probability model that determines hop timeout
        # TODO change to probability model using arrhenius equation
        if num_neighbor == 0:
            hop_interval = Config.migration_period_0neighbor
        elif num_neighbor == 1:
            hop_interval = Config.migration_period_1neighbor
        elif num_neighbor == 2:
            hop_interval = Config.migration_period_2neighbor
        elif num_neighbor == 3:
            hop_interval = Config.migration_period_3neighbor
        # elif num_neighbor == 4:
        #     hop_interval = Config.migration_period_4neighbor
        else:
            logger = logging.getLogger(__name__)
            logger.error('Invalid hop interval. ')
            hop_interval = -1
            raise ValueError('Invalid hop interval. ')
        return hop_interval

    @staticmethod
    def getEvaporationInterval(num_neighbor):
        # Probability model that determines evaporation timeout
        if num_neighbor == 0:
            evaporation_interval = Config.evaporation_period_0neighbor
        elif num_neighbor == 1:
            evaporation_interval = Config.evaporation_period_1neighbor
        elif num_neighbor == 2:
            evaporation_interval = Config.evaporation_period_2neighbor
        elif num_neighbor == 3:
            evaporation_interval = Config.evaporation_period_3neighbor
        # elif num_neighbor == 4:
        #     evaporation_interval = Config.evaporation_period_4neighbor
        else:
            logger = logging.getLogger(__name__)
            logger.error('Invalid evaporation interval. ')
            evaporation_interval = -1
            raise ValueError('Invalid evaporation interval. ')
        return evaporation_interval

    def updateNeighborTimeout(self):
        neighbors = self.getNeighbors()
        for neighbor in neighbors:
            num_neighbor = len(neighbor.getNeighbors())
            hop_interval = Atom.getHopInterval(num_neighbor)
            evaporation_interval = Atom.getEvaporationInterval(num_neighbor)
            logger = logging.getLogger(__name__)
            logger.debug("Atom %s at Site (%d,%d,%d) request migration interrupt with timeout %d. " % (neighbor.id, neighbor.position.x, neighbor.position.y, neighbor.position.k, hop_interval))
            logger.debug("Atom %s at Site (%d,%d,%d) request evaporation interrupt with timeout %d. " % (neighbor.id, neighbor.position.x, neighbor.position.y, neighbor.position.k, evaporation_interval))
            neighbor.process.interrupt((hop_interval, evaporation_interval))

    def run(self):
        logger = logging.getLogger(__name__)
        try:
            yield self.request
        except Exception, e:
            logger.error("Atom %s at Site (%d,%d,%d) interrupted. " % (self.id, self.position.x, self.position.y, self.position.k), exc_info=True)
            raise(e)
        migration_timeout = None
        evaporation_timeout = None
        ret = None
        site = self.field.getSite(self.position)
        site.atom = self
        logger.info("Clock %d Atom %s deposits at (%d,%d,%d). " % (self.env.now, self.id, self.position.x, self.position.y, self.position.k))
        self.updateNeighborTimeout()
        while True:

            hop_interval = Atom.getHopInterval(len(self.getNeighbors()))
            evaporation_interval = Atom.getEvaporationInterval(len(self.getNeighbors()))
            while True:
                try:
                    logger.debug("Atom %s at Site (%d,%d,%d) migration timeout %d. " % (self.id, self.position.x, self.position.y, self.position.k, hop_interval))
                    logger.debug("Atom %s at Site (%d,%d,%d) evaporation timeout %d. " % (self.id, self.position.x, self.position.y, self.position.k, evaporation_interval))
                    migration_timeout = self.env.timeout(hop_interval, 'migration')
                    evaporation_timeout = self.env.timeout(evaporation_interval, 'evaporation')
                    ret = yield migration_timeout | evaporation_timeout
                    logger.debug("Atom %s at Site (%d,%d,%d) resume. " % (self.id, self.position.x, self.position.y, self.position.k))
                    break
                except simpy.Interrupt as i:
                    logger.debug("Atom %s at Site (%d,%d,%d) migration timeout reset to %d. " % (self.id, self.position.x, self.position.y, self.position.k, i.cause[0]))
                    logger.debug("Atom %s at Site (%d,%d,%d) evaporation timeout reset to %d. " % (self.id, self.position.x, self.position.y, self.position.k, i.cause[1]))
                    (hop_interval, evaporation_interval) = i.cause
                except Exception, e:
                    logger.error("Atom %s at Site (%d,%d,%d) unknown interruption. " % (self.id, self.position.x, self.position.y, self.position.k), exc_info=True)
                    raise(e)
            if evaporation_timeout in ret:
                # remove the atom
                self.field.getSite(self.position).resource.release(self.request)
                self.field.getSite(self.position).atom = None
                self.updateNeighborTimeout()
                logger.debug('Atom %s updates its neighbors timeout.' % (self.id))
                logger.debug('Atom %s be removed. ' % (self.id))
                logger.info("Clock %d Atom %s evaporates from (%d,%d,%d). " % (self.env.now, self.id, self.position.x, self.position.y, self.position.k))
                return

            # get next hopping position
            next_position = self.getNextPosition()

            if self.field.getSite(next_position).resource.count != 0:
                if self.position == next_position:
                    logger.debug("Atom %s stays at Site (%d,%d,%d). " % (self.id, next_position.x, next_position.y, next_position.k))
                else:
                    logger.warning("Collision! Atom %s tries to hop to Site (%d,%d,%d) but occupied. No move. " % (self.id, next_position.x, next_position.y, next_position.k))

            else:
                self.field.getSite(self.position).resource.release(self.request)
                self.field.getSite(self.position).atom = None
                # Update previous neighbors time out
                self.updateNeighborTimeout()
                logger.debug('Atom %s updates old neighbors timeout.' % (self.id))

                self.request = self.field.getSite(next_position).resource.request()
                logger.debug('Atom %s requests to Site (%d,%d,%d).' % (self.id, next_position.x, next_position.y, next_position.k))
                try:
                    yield self.request
                except Exception, e:
                    logger.error("Atom %s at Site (%d,%d,%d) interrupted. Should not happen. " % (self.id, self.position.x, self.position.y, self.position.k), exc_info=True)
                    raise(e)

                logger.debug('Atom %s granted Site (%d,%d,%d).' % (self.id, next_position.x, next_position.y, next_position.k))
                logger.info('Clock %d Atom %s moves from (%d,%d,%d) to (%d,%d,%d).' % (self.env.now, self.id, next_position.x, next_position.y, self.position.k))
                site = self.field.getSite(next_position)
                site.atom = self
                self.position = next_position

                # Update new neighbors timeout.
                self.updateNeighborTimeout()
                # print('Atom %s updates new neighbors.' % (self.id))
                logger.debug('Atom %s updates new neighbors timeout.' % (self.id))

def deposition(field, env):
    # create atom by DEPOSITION_RATE
    # TODO Currently not probability model for efficiency reason.
    while True:
        yield env.timeout(1)
        deposition_rate = Config.DEPOSITION_RATE
        while deposition_rate >= 1:
            Atom.createAtom(field, env)
            deposition_rate -= 1
        if random.random() < deposition_rate:
            Atom.createAtom(field, env)

def clock(env):
    logger = logging.getLogger(__name__)
    while True:
        yield env.timeout(1)
        logger.debug("clock: %d" % env.now)


def main(beta_phi, beta_mu, repeat):
    log_path = 'logs/sim_betaphi%s_betamu%s%d' % (beta_phi, beta_mu, repeat)
    if os.path.exists(log_path):
        os.remove(log_path)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.INFO)

    # create a file handler
    handler = logging.FileHandler(log_path)
    handler.setLevel(logging.INFO)

    # create a logging format
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    Config.setParameters(beta_phi, beta_mu)
    now = datetime.datetime.now()
    logger.info(now.strftime("%Y-%m-%d %H:%M"))
    logger.info('Beta_Phi: %s Beta_Mu: %s' % (beta_phi, beta_mu))
    logger.info('Deposition rate per site: %s ' % Config.DEPOSITION_RATE_PER_SITE)
    logger.info("Simulation starts. #InitAtom: %d, Field: %d*%d, Time: %d" % (Config.NUM_ATOM, Config.SCOPE_SIZE, Config.SCOPE_SIZE, Config.SIM_TIME))
    if Config.SCOPE_SIZE * Config.SCOPE_SIZE * 2 < Config.NUM_ATOM:
        raise ValueError("Number of initial atom is too much")
    # Setup and start the simulation
    # random.seed(Config.RANDOM_SEED)  # This helps reproducing the results
    # Create an environment and start the setup process
    env = simpy.Environment()

    field = Field(env, Config.SCOPE_SIZE)
    Atom.id = 0
    Atom.createInitAtoms(field, env, Config.NUM_ATOM)

    env.process(clock(env))

    env.process(deposition(field, env))
    # Execute!
    env.run(until=Config.SIM_TIME)

    logger.handlers = []

if __name__ == '__main__':


    main(2.0, 2.0, 0)