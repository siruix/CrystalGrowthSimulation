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
    num_atoms = 0 # current total number of atoms
    field = None
    def __init__(self, id, env, position):
        self.id = id
        self.env = env
        self.position = position
        self.process = self.env.process(self.run())
        self.request = Atom.field.requestSite(position)
        Atom.field.setSiteAtom(position, self)

    @classmethod
    def createAtom(cls, env):
        # atom will not create if site occupied
        position = Position()
        if Atom.field.getSite(position).resource.count == 0:
            Atom.num_atoms += 1
            cls(Atom.id, env, position)
            Atom.id += 1

    @classmethod
    def createInitAtoms(cls, env, num_atom):
        # create all init atom in a batch
        Atom.id = 0
        while Atom.id < num_atom:
            # TODO improve efficiency
            # Must create atom
            while True:
                position = Position()
                if Atom.field.getSite(position).resource.count == 0:
                    Atom.num_atoms += 1
                    cls(Atom.id, env, position)
                    Atom.id += 1
                    break


    def getUnoccupiedNeighborDirections(self):
        # return a list of possible move direction
        # Now it's for one dimension
        possible_next_direction_list = []
        if Atom.field.getSite(Position.getNeighbor1Position(self.position)).resource.count == 0:
            possible_next_direction_list.append(Position.ONE)
        if Atom.field.getSite(Position.getNeighbor2Position(self.position)).resource.count == 0:
            possible_next_direction_list.append(Position.TWO)
        if Atom.field.getSite(Position.getNeighbor3Position(self.position)).resource.count == 0:
            possible_next_direction_list.append(Position.THREE)

        return possible_next_direction_list

    def getNextPositionAdAtom(self):
        # TODO next position affected by vicinity.
        # weighted average of all vicinity atoms on different rings
        # vicinity should be config
        # ring 0 is the direct neighbors
        # assume only be affected by ring 1
        positions = []
        if Atom.field.isSiteOccupied(Position.getNeighbor1Position(self.position)) is False:
            positions.append(Position.getNeighbor1Position(self.position))
        if Atom.field.isSiteOccupied(Position.getNeighbor2Position(self.position)) is False:
            positions.append(Position.getNeighbor2Position(self.position))
            # num_neighbor.append(Atom.getNumNeighbors(position2))
        if Atom.field.isSiteOccupied(Position.getNeighbor3Position(self.position)) is False:
            positions.append(Position.getNeighbor3Position(self.position))
            # num_neighbor.append(Atom.getNumNeighbors(position3))
        # find the largest num neighbor.
        positions.sort(key=lambda x: Atom.getNumNeighbors(x))
        num_neighbor = [Atom.getNumNeighbors(position) for position in positions]
        index = num_neighbor.index(num_neighbor[-1])
        rn = random.randint(index, len(positions)-1)
        return positions[rn]
        #
        #
        #
        #
        # if possible_next_direction_list[rn] == Position.ONE:
        #     next_position = Position.getNeighbor1Position(self.position)
        # elif possible_next_direction_list[rn] == Position.TWO:
        #     next_position = Position.getNeighbor2Position(self.position)
        # elif possible_next_direction_list[rn] == Position.THREE:
        #     next_position = Position.getNeighbor3Position(self.position)
        # else:
        #     next_position = self.position
        #     logger = logging.getLogger(__name__)
        #     logger.error("Invalid next position. ")
        # return next_position

    def getNextPositionDimmer(self):
        # Dimmer is considered as a whole. only consider first ring
        # return which atom lead the migration also
        neighbor = self.getNeighbors()[0]
        position = []
        if Position.getNeighbor1Position(self.position) != neighbor.position:
            position.append(Position.getNeighbor1Position(self.position))
        if Position.getNeighbor2Position(self.position) != neighbor.position:
            position.append(Position.getNeighbor2Position(self.position))
        if Position.getNeighbor3Position(self.position) != neighbor.position:
            position.append(Position.getNeighbor3Position(self.position))
        if Position.getNeighbor1Position(neighbor.position) != self.position:
            position.append(Position.getNeighbor1Position(self.position))
        if Position.getNeighbor2Position(neighbor.position) != self.position:
            position.append(Position.getNeighbor2Position(self.position))
        if Position.getNeighbor3Position(neighbor.position) != self.position:
            position.append(Position.getNeighbor3Position(self.position))

        position.sort(key=lambda x: Atom.getNumNeighbors(x))
        index = position.index(position[-1])
        rn = random.randint(index, len(position)-1)
        leader_atom = Atom.field.getSiteAtom(position[rn])
        return leader_atom,position[rn]

    @classmethod
    def getNumNeighbors(cls, position):
        num_neighbors = 0
        position1 = Position.getNeighbor1Position(position)
        position2 = Position.getNeighbor2Position(position)
        position3 = Position.getNeighbor3Position(position)    
        if Atom.field.isSiteOccupied(position1):
            num_neighbors += 1
        if Atom.field.isSiteOccupied(position2):
            num_neighbors += 1
        if Atom.field.isSiteOccupied(position3):
            num_neighbors += 1
        return num_neighbors

    def getNeighbors(self):
        # Define neighbor region. Here assume graphene 2D plane, which has up to 3 neighbors
        position1 = Position.getNeighbor1Position(self.position)
        position2 = Position.getNeighbor2Position(self.position)
        position3 = Position.getNeighbor3Position(self.position)

        neighbors = []
        if Atom.field.isSiteOccupied(position1):
            neighbors.append(Atom.field.getSiteAtom(position1))
        if Atom.field.isSiteOccupied(position2):
            neighbors.append(Atom.field.getSiteAtom(position2))
        if Atom.field.isSiteOccupied(position3):
            neighbors.append(Atom.field.getSiteAtom(position3))

        return neighbors

    def isRing(self):
        if Atom.getNumNeighbors(self.position) <= 1:
            return False
        position1 = Position.getNeighbor1Position(self.position)
        if Atom.field.isSiteOccupied(position1):
            position12 = Position.getNeighbor2Position(position1)
            if Atom.field.isSiteOccupied(position12):
                position123 = Position.getNeighbor3Position(position12)
                if Atom.field.isSiteOccupied(position123):
                    position1231 = Position.getNeighbor1Position(position123)
                    if Atom.field.isSiteOccupied(position1231):
                        position12312 = Position.getNeighbor2Position(position1231)
                        if Atom.field.isSiteOccupied(position12312):
                            return True

            position13 = Position.getNeighbor3Position(position1)
            if Atom.field.isSiteOccupied(position13):
                position132 = Position.getNeighbor2Position(position13)
                if Atom.field.isSiteOccupied(position132):
                    position1321 = Position.getNeighbor1Position(position132)
                    if Atom.field.isSiteOccupied(position1321):
                        position13213 = Position.getNeighbor3Position(position1321)
                        if Atom.field.isSiteOccupied(position13213):
                            return True

        position2 = Position.getNeighbor2Position(self.position)
        if Atom.field.isSiteOccupied(position2):
            position21 = Position.getNeighbor1Position(position2)
            if Atom.field.isSiteOccupied(position21):
                position213 = Position.getNeighbor3Position(position21)
                if Atom.field.isSiteOccupied(position213):
                    position2132 = Position.getNeighbor2Position(position213)
                    if Atom.field.isSiteOccupied(position2132):
                        position21321 = Position.getNeighbor2Position(position2132)
                        if Atom.field.isSiteOccupied(position21321):
                            return True
        return False

    def isAdAtom(self):
        return True if Atom.getNumNeighbors(self.position) == 0 else False
    
    def isDimmer(self):
        if Atom.getNumNeighbors(self.position) != 1:
            return False
        position1 = Position.getNeighbor1Position(self.position)
        if Atom.field.isSiteOccupied(position1) and Atom.getNumNeighbors(position1) == 1:
            return True

        position2 = Position.getNeighbor2Position(self.position)
        if Atom.field.isSiteOccupied(position2) and Atom.getNumNeighbors(position2) == 1:
            return True

        position3 = Position.getNeighbor3Position(self.position)
        if Atom.field.isSiteOccupied(position3) and Atom.getNumNeighbors(position3) == 1:
            return True

    def isEvaporate(self):
        # assume atom in a ring is not able to evaporate
        if self.isRing() is True:
            return False
        evaporation_rate = Config.evaporation_rate_by_num_neighbor[Atom.getNumNeighbors(self.position)]
        if random.random() < evaporation_rate:
            return True
        else:
            return False

    def isMigrate(self):
        # TODO migration affected vicinity neighbor
        migration_rate = Config.migration_rate_by_num_neighbor[Atom.getNumNeighbors(self.position)]
        if random.random() < migration_rate:
            return True
        else:
            return False

    def releaseSite(self):
        Atom.field.releaseSite(self.position, self.request)
        Atom.field.setSiteAtom(self.position, None)

    def requestSite(self, position):
        Atom.field.setSiteAtom(position, self)
        self.position = position


    def run(self):
        logger = logging.getLogger(__name__)
        logger.info("Clock %d Atom %s deposits at (%d,%d,%d). " % (self.env.now, self.id, self.position.x, self.position.y, self.position.k))
        yield self.request
        while True:
            while True:
                try:
                    yield self.env.timeout(1)
                    logger.debug("Atom %s at Site (%d,%d,%d) check. " % (self.id, self.position.x, self.position.y, self.position.k))
                    break
                except simpy.Interrupt as i:
                    # migrate the interrupted dimmer
                    next_position = i.cause
                    logger.debug("Atom %s migration to (%d,%d,%d). " % (self.id, next_position.x, next_position.y, next_position.k))
                    self.releaseSite()
                    self.request = Atom.field.requestSite(next_position)
                    # logger.debug('Atom %s requests to Site (%d,%d,%d).' % (self.id, next_position.x, next_position.y, next_position.k))
                    # logger.debug('Atom %s granted Site (%d,%d,%d).' % (self.id, next_position.x, next_position.y, next_position.k))
                    logger.info('Clock %d Atom %s moves from (%d,%d,%d) to (%d,%d,%d).' % (self.env.now, self.id, self.position.x, self.position.y, self.position.k, next_position.x, next_position.y, next_position.k))
                    self.requestSite(next_position)
                    # try:
                    yield self.request
                    # except Exception, e:
                    #     logger.error("Atom %s at Site (%d,%d,%d) interrupted. Should not happen. " % (self.id, self.position.x, self.position.y, self.position.k), exc_info=True)
                    #     raise(e)

                except Exception, e:
                    logger.error("Atom %s at Site (%d,%d,%d) unknown interruption. " % (self.id, self.position.x, self.position.y, self.position.k), exc_info=True)
                    raise(e)

            if self.isEvaporate() is True:
                self.releaseSite()
                Atom.num_atoms -= 1
                logger.info("Clock %d Atom %s evaporates from (%d,%d,%d). " % (self.env.now, self.id, self.position.x, self.position.y, self.position.k))
                return      # stop such process when return

            elif self.isMigrate() is True:
                # assume only ad-atom or dimmer migration

                if self.isAdAtom():
                    # ad-atom migration
                    next_position = self.getNextPositionAdAtom()
                    self.releaseSite()
                    # Atom.field.getSite(self.position).resource.release(self.request)
                    # Atom.field.getSite(self.position).atom = None
                    self.request = Atom.field.requestSite(next_position)
                    logger.debug('Atom %s requests to Site (%d,%d,%d). Ad-atom migration' % (self.id, next_position.x, next_position.y, next_position.k))
                    self.requestSite(next_position)
                    # logger.debug('Atom %s granted Site (%d,%d,%d).' % (self.id, next_position.x, next_position.y, next_position.k))
                    logger.info('Clock %d Atom %s moves from (%d,%d,%d) to (%d,%d,%d).' % (self.env.now, self.id, self.position.x, self.position.y, self.position.k, next_position.x, next_position.y, next_position.k))
                    yield self.request

                elif self.isDimmer():
                    # dimmer migration
                    neighbors = self.getNeighbors()
                    neighbor = neighbors[0]
                    leader, next_position = self.getNextPositionDimmer()
                    if leader == self:
                        neighbor_next_position = self.position
                        self.releaseSite()
                        self.request = Atom.field.requestSite(next_position)
                        logger.debug('Atom %s requests to Site (%d,%d,%d). Dimmer migration. Neighbor: %d' % (self.id, next_position.x, next_position.y, next_position.k, neighbor.id))
                        # logger.debug('Atom %s granted Site (%d,%d,%d).' % (self.id, next_position.x, next_position.y, next_position.k))
                        logger.info('Clock %d Atom %s moves from (%d,%d,%d) to (%d,%d,%d).' % (self.env.now, self.id, self.position.x, self.position.y, self.position.k, next_position.x, next_position.y, next_position.k))
                        self.requestSite(next_position)
                        # neighbor must be interrupt and migrate
                        neighbor.process.interrupt(neighbor_next_position)

                        # try:
                        yield self.request
                        # except Exception, e:
                        #     logger.error("Atom %s at Site (%d,%d,%d) interrupted. Should not happen. " % (self.id, self.position.x, self.position.y, self.position.k), exc_info=True)
                        #     raise(e)
                    else:
                        # use fake migration. tunneling self to next_position
                        self.releaseSite()
                        self.request = Atom.field.requestSite(next_position)
                        logger.debug('Atom %s requests to Site (%d,%d,%d). Dimmer tunnel migration. Neighbor: %d' % (self.id, next_position.x, next_position.y, next_position.k, neighbor.id))
                        # logger.debug('Atom %s granted Site (%d,%d,%d).' % (self.id, next_position.x, next_position.y, next_position.k))
                        logger.info('Clock %d Atom %s moves from (%d,%d,%d) to (%d,%d,%d).' % (self.env.now, self.id, self.position.x, self.position.y, self.position.k, next_position.x, next_position.y, next_position.k))
                        self.requestSite(next_position)
                        yield self.request

                else: # other cluster size do not migrate
                    logger.debug('Atom %s is a large cluster. no move' % (self.id))
            else:
                logger.debug('Atom %s neither evaporate nor migrate' % (self.id))

def deposition(env):
    # create atom by DEPOSITION_RATE
    # TODO Currently not probability model for efficiency reason.
    while True:
        yield env.timeout(1)
        if Atom.num_atoms >= Config.SCOPE_SIZE * Config.SCOPE_SIZE * 2:
            raise ValueError('Coverage 100% ')
        deposition_rate = Config.DEPOSITION_RATE
        while deposition_rate >= 1:
            Atom.createAtom(env)
            deposition_rate -= 1
        if random.random() < deposition_rate:
            Atom.createAtom(env)

def clock(env):
    logger = logging.getLogger(__name__)
    while True:
        yield env.timeout(1)
        logger.debug("clock: %d" % env.now)


def main(beta_phi, beta_mu, repeat, log_level):
    log_path = 'logs/sim_betaphi%s_betamu%s%d' % (beta_phi, beta_mu, repeat)
    if os.path.exists(log_path):
        os.remove(log_path)
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
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
    random.seed(Config.RANDOM_SEED)  # This helps reproducing the results
    # Create an environment and start the setup process
    env = simpy.Environment()

    field = Field(env, Config.SCOPE_SIZE)
    Atom.id = 0
    Atom.field = field
    Atom.num_atoms = 0
    Atom.createInitAtoms(env, Config.NUM_ATOM)

    env.process(clock(env))

    env.process(deposition(env))
    # Execute!
    env.run(until=Config.SIM_TIME)

    logger.handlers = []

if __name__ == '__main__':


    main(5.0, 3.0, 0, logging.DEBUG)