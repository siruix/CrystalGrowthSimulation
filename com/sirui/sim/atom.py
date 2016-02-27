from com.sirui.sim.context import Context
from com.sirui.sim.position import Position
import random
from com.sirui.sim.config import Config
import logging
import simpy
import abc

# abstract class
class AbstractAtom(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.status = 'Active'
        self.reactivate = Context.getEnv().event()

    @classmethod
    def createOne(cls):
        raise NotImplementedError

    @classmethod
    def createInit(cls, num_atom):
        raise NotImplementedError

    def getNumNeighbors(self):
        num_neighbors = 0
        positions = Position.getNeighborPositions(self.position)
        for position in positions:
            if Context.getField().isSiteOccupied(position):
                num_neighbors += 1
        return num_neighbors

    # def getNumSameHeightNeighbors(self):
    #     num_neighbors = 0
    #     positions = Position.getSameHeightNeighborPositions(self.position)
    #     for position in positions:
    #         if Context.getField().isSiteOccupied(position):
    #             num_neighbors += 1
    #     return num_neighbors


    @abc.abstractmethod
    def isDesorb(self):
        """determine if such atom evaporate"""
        return

    @abc.abstractmethod
    def isDiffuse(self):
        return

    @abc.abstractmethod
    def releaseSite(self):
        return

    @abc.abstractmethod
    def requestSite(self, position):
        return

    @abc.abstractmethod
    def run(self):
        """atom process"""
        return


class Atom(AbstractAtom):
    id = 0
    num = 0
    def __init__(self, id, position):
        super(Atom, self).__init__(id, position)
        self.process = Context.getEnv().process(self.run())
        Context.addAtom(self)
        self.request = Context.getField().requestSite(position)
        Context.getField().setSiteAtom(position, self)
        # deactivate the atom underneath
        self.deactivate()

    @classmethod
    def createInit(cls, num):
        cls.id = 0
        while cls.id < num:
            while True:
                position = Position()
                if not Context.getField().isSiteOccupied(position):
                    cls.num += 1
                    cls(cls.id, position)
                    cls.id += 1
                    break

    @classmethod
    def createOne(cls):
        # create one at lowest position
        position = Position()
        position = Context.getField().getLowestUnoccupiedPosition(position.x, position.y)
        if position is None:
            return
        cls.num += 1
        cls(cls.id, position)
        cls.id += 1

    def deactivate(self):
        if self.position.z == 0:
            return
        # only deactivate atom underneath
        atom = Context.getField().getSiteAtom(Position.getDownPosition(self.position))
        atom.process.interrupt(('Freeze', self))


    def releaseSite(self):
        Context.getField().releaseSite(self.position, self.request)
        Context.getField().setSiteAtom(self.position, None)

    def requestSite(self, position):
        Context.getField().setSiteAtom(position, self)
        self.position = position

    def isDesorb(self):
        # only surface atom evaporate
        if not Context.getField().isSurface(self.position):
            return False
        # evaporation rate depends on direct neighbors
        rate = 0
        num_neighbor = self.getNumNeighbors()
        if num_neighbor == 0: # free adatom
            rate = Config.desorption_rate_by_num_neighbor[0]
        if num_neighbor == 1:
            rate = Config.desorption_rate_by_num_neighbor[1]
        if num_neighbor == 2: # kink atom.
            rate = Config.desorption_rate_by_num_neighbor[2]
        if num_neighbor == 3:
            rate = Config.desorption_rate_by_num_neighbor[3]
        if num_neighbor == 4:
            rate = Config.desorption_rate_by_num_neighbor[4]
        if num_neighbor == 5:
            rate = Config.desorption_rate_by_num_neighbor[5]

        if random.random() < rate:
            return True
        else:
            return False

    def isDiffuse(self):
        # only surface atom diffuse.
        if not Context.getField().isSurface(self.position):
            return False
        rate = 0
        num_neighbor = self.getNumNeighbors()
        if num_neighbor == 0: # free adatom
            rate = Config.diffusion_rate_by_num_neighbor[0]
        if num_neighbor == 1:
            rate = Config.diffusion_rate_by_num_neighbor[1]
        if num_neighbor == 2: # kink atom.
            rate = Config.diffusion_rate_by_num_neighbor[2]
        if num_neighbor == 3:
            rate = Config.diffusion_rate_by_num_neighbor[3]
        if num_neighbor == 4:
            rate = Config.diffusion_rate_by_num_neighbor[4]
        if num_neighbor == 5:
            rate = Config.diffusion_rate_by_num_neighbor[5]

        if random.random() < rate:
            return True
        else:
            return False

    def getNextPosition(self):
        # Diffusion is one-way down.
        positions = Position.getSameHeightNeighborPositions(self.position)
        unoccupied_positions = []
        for position in positions:
            if not Context.getField().isSiteOccupied(position):
                unoccupied_positions.append(position)
        if len(unoccupied_positions) == 0:
            return self.position
        rn = random.randint(0, len(unoccupied_positions)-1)
        position = unoccupied_positions[rn]
        return Context.getField().getLowestUnoccupiedPosition(position.x, position.y)

    def run(self):
        logger = logging.getLogger()
        logger.info("Clock %d Atom %s adsorb at (%d,%d,%d). " % (Context.getEnv().now, self.id, self.position.x, self.position.y, self.position.z))
        while True:
            try:
                yield self.request
                break
            except simpy.Interrupt as i:
                (reason, info) = i.cause
                if reason == 'Stop':
                    self.status = 'Stop'
                elif reason == 'Freeze':
                    self.status = 'Freeze'
                    self.info = info
                else:
                    raise ValueError('Unknown interruption! ')

        while True:
            while True:
                if self.status == 'Active':
                    try:
                        yield Context.getEnv().timeout(1)
                        logger.debug("Atom %s at Site (%d,%d,%d) check. " % (self.id, self.position.x, self.position.y, self.position.z))
                        break
                    except simpy.Interrupt as i:
                        (reason, info) = i.cause
                        if reason == 'Stop':
                            self.status = 'Stop'
                        elif reason == 'Freeze':
                            self.status = 'Freeze'
                            self.info = info
                        else:
                            raise ValueError('Impossible interruption reason! ')
                    except Exception, e:
                        logger.error("Atom %s at Site (%d,%d,%d) impossible interruption type. " % (self.id, self.position.x, self.position.y, self.position.k), exc_info=True)
                        raise(e)

                elif self.status == 'Freeze':
                    wait_for = self.info
                    try:
                        yield wait_for.reactivate
                        self.status = 'Active'
                        logger.debug('Atom %s at Site (%d,%d,%d) reactivated. % (self.id, self.position.x, self.position.y, self.position.k)')
                    except simpy.Interrupt as i:
                        (reason, info) = i.cause
                        if reason == 'Stop':
                            self.status = 'Stop'
                        else:
                            raise ValueError('Impossible interruption reason! ')
                    except Exception, e:
                        logger.error("Atom %s at Site (%d,%d,%d) impossible interruption type. " % (self.id, self.position.x, self.position.y, self.position.k), exc_info=True)
                        raise(e)

                elif self.status == 'Stop':
                    Context.removeAtom(self)
                    self.reactivate.succeed()  # reactivate atom underneath
                    logger.debug('Atom %s process terminated' % self.id)
                    return
                else:
                    raise ValueError('Unknown statues! ')

            if self.isDesorb():
                # evaporation affected only by neighbors
                self.releaseSite()
                self.num -= 1
                logger.info("Clock %d Atom %s desorb from (%d,%d,%d). " % (Context.getEnv().now, self.id, self.position.x, self.position.y, self.position.z))
                self.status = 'Stop'

            elif self.isDiffuse():
                next_position = self.getNextPosition()
                self.releaseSite()
                self.request = Context.getField().requestSite(next_position)
                logger.debug('Atom %s requests to Site (%d,%d,%d). Migration' % (self.id, next_position.x, next_position.y, next_position.z))
                logger.info('Clock %d Atom %s diffuse from (%d,%d,%d) to (%d,%d,%d).' % (Context.getEnv().now, self.id, self.position.x, self.position.y, self.position.z, next_position.x, next_position.y, next_position.z))
                self.requestSite(next_position)
                self.reactivate.succeed()
                self.reactivate = Context.getEnv().event()
                while True:
                    try:
                        yield self.request
                        break
                    except simpy.Interrupt as i:
                        (reason, info) = i.cause
                        if reason == 'Stop':
                            self.status = 'Stop'
                        elif reason == 'Freeze':
                            self.status = 'Freeze'
                            self.info = info
                        else:
                            raise ValueError('Unknown interruption! ')

            else:
                logger.debug('Atom %s no change' % (self.id))

