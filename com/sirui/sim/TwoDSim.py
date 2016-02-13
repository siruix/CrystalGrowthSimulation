from __future__ import print_function
import random
import logging
import os
import datetime
import time
from com.sirui.sim.resources import *
from com.sirui.sim.context import *
from com.sirui.sim.config import Config
from com.sirui.sim.position import Position
from com.sirui.sim.utility import *

class Atom(object):
    id = 0 # keep track latest id
    num_atoms = 0 # current total number of atoms
    # field = None
    def __init__(self, id, env, position):
        self.id = id
        self.env = env
        self.position = position
        self.process = self.env.process(self.run())
        Context.addAtom(self)
        self.request = Context.getField().requestSite(position)
        Context.getField().setSiteAtom(position, self)

    @classmethod
    def createAtom(cls, env):
        # atom will not create if site occupied
        position = Position()
        if Context.getField().getSite(position).resource.count == 0:
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
                if Context.getField().getSite(position).resource.count == 0:
                    Atom.num_atoms += 1
                    cls(Atom.id, env, position)
                    Atom.id += 1
                    break


    def getUnoccupiedNeighborDirections(self):
        # return a list of possible move direction
        # Now it's for one dimension
        possible_next_direction_list = []
        positions = Position.getNeighborPositions(self.position)
        for i,position in enumerate(positions):
            if Context.getField().isSiteOccupied(position) is False:
                possible_next_direction_list.append(i)

        return possible_next_direction_list

    def getAtomMigratePosition(self):
        positions = Position.getNeighborPositions(self.position)
        unoccupied_positions = []
        for position in positions:
            if Context.getField().isSiteOccupied(position) is False:
                unoccupied_positions.append(position)
        if len(unoccupied_positions) == 0:
            return self.position
        rn = random.randint(0, len(unoccupied_positions)-1)
        return unoccupied_positions[rn]

    def getAdAtomNextPosition(self):
        # TODO next position affected by vicinity.
        # weighted average of all vicinity atoms on different rings
        # vicinity should be config
        # ring 0 is the direct neighbors
        # assume only be affected by ring 1
        positions = []
        for position in Position.getNeighborPositions(self.position):
            if Context.getField().isSiteOccupied(position) is False:
                positions.append(position)

        positions.sort(key=lambda x: Atom.getNumNeighbors(x))
        num_neighbor = [Atom.getNumNeighbors(position) for position in positions]
        index = num_neighbor.index(num_neighbor[-1])
        rn = random.randint(index, len(positions)-1)
        return positions[rn]

    def getDimerPair(self):
        return self.getNeighbors()[0]

    def getDimer(self):
        pass

    def getDimerNextPosition(self):
        # Dimer is considered as a whole. only consider first ring
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
        leader_atom = Context.getField().getSiteAtom(position[rn])
        return leader_atom,position[rn]

    def getTrimer(self):
        # return a list of positions of trimer cluster
        pass

    @classmethod
    def getNumNeighbors(cls, position):
        num_neighbors = 0
        positions = Position.getNeighborPositions(position)
        for position in positions:
            if Context.getField().isSiteOccupied(position):
                num_neighbors += 1
        return num_neighbors

    def getNumDeLocalised(self):
        delocalized_atom_position = set({})
        position1 = Position.getNeighbor1Position(self.position)
        if Context.getField().isSiteOccupied(position1):
            delocalized_atom_position.add(position1)
            position12 = Position.getNeighbor2Position(position1)
            position13 = Position.getNeighbor3Position(position1)

            if Context.getField().isSiteOccupied(position12):
                delocalized_atom_position.add(position12)
                position123 = Position.getNeighbor3Position(position12)
                if Context.getField().isSiteOccupied(position123):
                    delocalized_atom_position.add(position123)
                    position1231 = Position.getNeighbor3Position(position123)
                    if Context.getField().isSiteOccupied(position1231):
                        delocalized_atom_position.add(position1231)

            if Context.getField().isSiteOccupied(position13):
                delocalized_atom_position.add(position13)
                position132 = Position.getNeighbor2Position(position13)
                if Context.getField().isSiteOccupied(position132):
                    delocalized_atom_position.add(position132)
                    position1321 = Position.getNeighbor1Position(position132)
                    if Context.getField().isSiteOccupied(position1321):
                        delocalized_atom_position.add(position1321)

        position2 = Position.getNeighbor2Position(self.position)
        if Context.getField().isSiteOccupied(position2):
            delocalized_atom_position.add(position2)
            position21 = Position.getNeighbor1Position(position2)
            position23 = Position.getNeighbor3Position(position2)

            if Context.getField().isSiteOccupied(position21):
                delocalized_atom_position.add(position21)
                position213 = Position.getNeighbor3Position(position21)
                if Context.getField().isSiteOccupied(position213):
                    delocalized_atom_position.add(position213)
                    position2132 = Position.getNeighbor2Position(position213)
                    if Context.getField().isSiteOccupied(position2132):
                        delocalized_atom_position.add(position2132)

            if Context.getField().isSiteOccupied(position23):
                delocalized_atom_position.add(position23)
                position231 = Position.getNeighbor1Position(position23)
                if Context.getField().isSiteOccupied(position231):
                    delocalized_atom_position.add(position231)
                    position2312 = Position.getNeighbor2Position(position231)
                    if Context.getField().isSiteOccupied(position2312):
                        delocalized_atom_position.add(position2312)

        position3 = Position.getNeighbor3Position(self.position)
        if Context.getField().isSiteOccupied(position3):
            delocalized_atom_position.add(position3)
            position31 = Position.getNeighbor1Position(position3)
            position32 = Position.getNeighbor2Position(position3)

            if Context.getField().isSiteOccupied(position31):
                delocalized_atom_position.add(position31)
                position312 = Position.getNeighbor2Position(position31)
                if Context.getField().isSiteOccupied(position312):
                    delocalized_atom_position.add(position312)
                    position3123 = Position.getNeighbor3Position(position312)
                    if Context.getField().isSiteOccupied(position3123):
                        delocalized_atom_position.add(position3123)

            if Context.getField().isSiteOccupied(position32):
                delocalized_atom_position.add(position32)
                position321 = Position.getNeighbor1Position(position32)
                if Context.getField().isSiteOccupied(position321):
                    delocalized_atom_position.add(position321)
                    position3213 = Position.getNeighbor3Position(position321)
                    if Context.getField().isSiteOccupied(position3213):
                        delocalized_atom_position.add(position3213)

        return len(delocalized_atom_position)

    def getNeighbors(self):
        # direct neighbor atom
        positions = Position.getNeighborPositions(self.position)
        neighbors = []
        for position in positions:
            if Context.getField().isSiteOccupied(position):
                neighbors.append(Context.getField().getSiteAtom(position))
        return neighbors

    def isRing(self):
        if Atom.getNumNeighbors(self.position) <= 1:
            return False
        position1 = Position.getNeighbor1Position(self.position)
        if Context.getField().isSiteOccupied(position1):
            position12 = Position.getNeighbor2Position(position1)
            if Context.getField().isSiteOccupied(position12):
                position123 = Position.getNeighbor3Position(position12)
                if Context.getField().isSiteOccupied(position123):
                    position1231 = Position.getNeighbor1Position(position123)
                    if Context.getField().isSiteOccupied(position1231):
                        position12312 = Position.getNeighbor2Position(position1231)
                        if Context.getField().isSiteOccupied(position12312):
                            return True

            position13 = Position.getNeighbor3Position(position1)
            if Context.getField().isSiteOccupied(position13):
                position132 = Position.getNeighbor2Position(position13)
                if Context.getField().isSiteOccupied(position132):
                    position1321 = Position.getNeighbor1Position(position132)
                    if Context.getField().isSiteOccupied(position1321):
                        position13213 = Position.getNeighbor3Position(position1321)
                        if Context.getField().isSiteOccupied(position13213):
                            return True

        position2 = Position.getNeighbor2Position(self.position)
        if Context.getField().isSiteOccupied(position2):
            position21 = Position.getNeighbor1Position(position2)
            if Context.getField().isSiteOccupied(position21):
                position213 = Position.getNeighbor3Position(position21)
                if Context.getField().isSiteOccupied(position213):
                    position2132 = Position.getNeighbor2Position(position213)
                    if Context.getField().isSiteOccupied(position2132):
                        position21321 = Position.getNeighbor2Position(position2132)
                        if Context.getField().isSiteOccupied(position21321):
                            return True
        return False

    def connectedAtoms(self):
        # find all connected atoms and return a list
        connected_atoms = [self]
        queue = [self]
        while len(queue) != 0:
            atom = queue.pop(0)
            for neighbor in atom.getNeighbors():
                if neighbor not in connected_atoms:
                    connected_atoms.append(neighbor)
                    queue.append(neighbor)
            if len(connected_atoms) > 10: # early termination if cluster size too large
                return None
        return connected_atoms

    def isAdAtom(self):
        return True if Atom.getNumNeighbors(self.position) == 0 else False
    
    def isDimer(self):
        if Atom.getNumNeighbors(self.position) != 1:
            return False
        positions = Position.getNeighborPositions(self.position)
        for position in positions:
            if Context.getField().isSiteOccupied(position) and Atom.getNumNeighbors(position) == 1:
                return True

    def isTrimer(self):
        if self.connectedAtoms() is None:
            return False
        return True if len(self.connectedAtoms()) == 3 else False

    def isStrongBond(self):
        return False

    def isEvaporate(self):
        # evaporation rate depends on direct neighbors
        # depends on zigzag armchair edge
        # depends on p-electron de-localization
        # assume p-electron only present within three neighbor rings.
        rate = 0
        num_neighbor = Atom.getNumNeighbors(self.position)
        if num_neighbor == 0: # free adatom
            rate = Config.evaporation_rate_by_num_neighbor[0]
        if num_neighbor == 1: # dangling atom
            rate = Config.evaporation_rate_by_num_neighbor[1]
        if num_neighbor == 2: # edge atom.
            # delocalize effect mostly at edge
            rate = Config.evaporation_rate_by_num_neighbor[2] * Config.delocalized_rate[self.getNumDeLocalised()]

        if num_neighbor == 3:
            evaporation_rate = Config.evaporation_rate_by_num_neighbor[3]
            num_delocalized = self.getNumDeLocalised() # 0 - 12
            rate = evaporation_rate * Config.delocalized_rate[num_delocalized]
        if random.random() < rate:
            return True
        else:
            return False

    def isMigrate(self):
        # TODO more strong delocalizing effect
        # TODO zigzag armchair
        num_neighbor = Atom.getNumNeighbors(self.position)
        migrate_rate = Config.migration_rate_by_num_neighbor[num_neighbor]
        num_delocalized = self.getNumDeLocalised() # 0 - 12
        rate = migrate_rate * Config.delocalized_rate[num_delocalized]
        if random.random() < rate:
            return True
        else:
            return False

    def isAdAtomMigrate(self):
        # migration rate affected by vicinity neighbors
        # TODO config vicinity range
        migration_rate = Config.getAdAtomMigrationRate()
        if random.random() < migration_rate:
            return True
        else:
            return False

    def isDimerDrift(self):
        # migration rate affected by vicinity neighbors. Larger the cluster size, less rate
        # TODO config vicinity range
        migration_rate = Config.getDimerMigrationRate()
        if random.random() < migration_rate:
            return True
        else:
            return False

    def isTrimerMigrate(self):
        # migration rate affected by vicinity neighbors. Larger the cluster size, less rate
        # TODO config vicinity range
        migration_rate = Config.migration_rate_by_num_neighbor[Atom.getNumNeighbors(self.position)] / 3
        if random.random() < migration_rate:
            return True
        else:
            return False

    def releaseSite(self):
        Context.getField().releaseSite(self.position, self.request)
        Context.getField().setSiteAtom(self.position, None)

    def requestSite(self, position):
        Context.getField().setSiteAtom(position, self)
        self.position = position


    def run(self):
        logger = logging.getLogger(__name__)
        logger.info("Clock %d Atom %s deposits at (%d,%d,%d). " % (self.env.now, self.id, self.position.x, self.position.y, self.position.k))
        try:
            yield self.request
        except simpy.Interrupt as i:
            (reason, info) = i.cause
            if reason == 'Stop':
                Context.removeAtom(self)
                print('Atom %s process terminated' % self.id)
                return
            else:
                raise ValueError('Unknown interruption! ')

        while True:
            while True:
                try:
                    yield self.env.timeout(1)
                    logger.debug("Atom %s at Site (%d,%d,%d) check. " % (self.id, self.position.x, self.position.y, self.position.k))
                    break
                except simpy.Interrupt as i:
                    (reason, info) = i.cause
                    # migrate the interrupted Dimer
                    if reason == 'migrate':
                        next_position = info
                        logger.debug("Atom %s migration to (%d,%d,%d). " % (self.id, next_position.x, next_position.y, next_position.k))
                        self.releaseSite()
                        self.request = Context.getField().requestSite(next_position)
                        logger.info('Clock %d Atom %s moves from (%d,%d,%d) to (%d,%d,%d).' % (self.env.now, self.id, self.position.x, self.position.y, self.position.k, next_position.x, next_position.y, next_position.k))
                        self.requestSite(next_position)
                        try:
                            yield self.request
                        except simpy.Interrupt as i:
                            (reason, info) = i.cause
                            if reason == 'Stop':
                                Context.removeAtom(self)
                                print('Atom %s process terminated' % self.id)
                                return
                            else:
                                raise ValueError('Unknown interruption! ')

                    elif reason == 'Stop':
                        Context.removeAtom(self)
                        print('Atom %s process terminated' % self.id)
                        return

                    else:
                        raise ValueError('Unknown interruption! ')

                except Exception, e:
                    logger.error("Atom %s at Site (%d,%d,%d) unknown interruption. " % (self.id, self.position.x, self.position.y, self.position.k), exc_info=True)
                    raise(e)

            if self.isEvaporate() is True:
                # evaporation affected only by neighbors
                self.releaseSite()
                Atom.num_atoms -= 1
                logger.info("Clock %d Atom %s evaporates from (%d,%d,%d). " % (self.env.now, self.id, self.position.x, self.position.y, self.position.k))
                Context.removeAtom(self)
                return      # stop such process when return

            # check if atom migrate
            if self.isMigrate() is True:
                next_position = self.getAtomMigratePosition()
                self.releaseSite()
                self.request = Context.getField().requestSite(next_position)
                logger.debug('Atom %s requests to Site (%d,%d,%d). Ad-atom migration' % (self.id, next_position.x, next_position.y, next_position.k))
                logger.info('Clock %d Atom %s moves from (%d,%d,%d) to (%d,%d,%d).' % (self.env.now, self.id, self.position.x, self.position.y, self.position.k, next_position.x, next_position.y, next_position.k))
                self.requestSite(next_position)
                try:
                    yield self.request
                except simpy.Interrupt as i:
                    (reason, info) = i.cause
                    if reason == 'Stop':
                        Context.removeAtom(self)
                        print('Atom %s process terminated' % self.id)
                        return
                    else:
                        raise ValueError('Unknown interruption! ')

            # if self.isAdAtom() and self.isAdAtomMigrate():
            #     # ad-atom migration
            #     next_position = self.getAdAtomNextPosition()
            #     self.releaseSite()
            #     self.request = Context.getField().requestSite(next_position)
            #     logger.debug('Atom %s requests to Site (%d,%d,%d). Ad-atom migration' % (self.id, next_position.x, next_position.y, next_position.k))
            #     self.requestSite(next_position)
            #     logger.info('Clock %d Atom %s moves from (%d,%d,%d) to (%d,%d,%d).' % (self.env.now, self.id, self.position.x, self.position.y, self.position.k, next_position.x, next_position.y, next_position.k))
            #     yield self.request

            # cluster up to certain size enable migration
            if self.isDimer() and self.isDimerDrift():
                # Dimer migration
                neighbor = self.getDimerPair()
                leader, next_position = self.getDimerNextPosition()
                if leader == self:
                    neighbor_next_position = self.position
                    self.releaseSite()
                    self.request = Context.getField().requestSite(next_position)
                    logger.debug('Atom %s requests to Site (%d,%d,%d). Dimer migration. Neighbor: %d' % (self.id, next_position.x, next_position.y, next_position.k, neighbor.id))
                    logger.info('Clock %d Atom %s moves from (%d,%d,%d) to (%d,%d,%d).' % (self.env.now, self.id, self.position.x, self.position.y, self.position.k, next_position.x, next_position.y, next_position.k))
                    self.requestSite(next_position)
                    neighbor.process.interrupt(('migrate', neighbor_next_position))
                    try:
                        yield self.request
                    except simpy.Interrupt as i:
                        (reason, info) = i.cause
                        if reason == 'Stop':
                            Context.removeAtom(self)
                            print('Atom %s process terminated' % self.id)
                            return
                        else:
                            raise ValueError('Unknown interruption! ')

                else:
                    # use fake migration. tunneling self to next_position
                    self.releaseSite()
                    self.request = Context.getField().requestSite(next_position)
                    logger.debug('Atom %s requests to Site (%d,%d,%d). Dimer tunnel migration. Neighbor: %d' % (self.id, next_position.x, next_position.y, next_position.k, neighbor.id))
                    logger.info('Clock %d Atom %s moves from (%d,%d,%d) to (%d,%d,%d).' % (self.env.now, self.id, self.position.x, self.position.y, self.position.k, next_position.x, next_position.y, next_position.k))
                    self.requestSite(next_position)
                    # with yield_guard(self.request, self.id) as yg:
                    #     pass
                    try:
                        yield self.request
                    except simpy.Interrupt as i:
                        (reason, info) = i.cause
                        if reason == 'Stop':
                            Context.removeAtom(self)
                            print('Atom %s process terminated' % self.id)
                            return
                        else:
                            raise ValueError('Unknown interruption! ')

            # elif self.isTrimer() and self.isTrimerMigrate():
            #     #
            else:
                # general migration
                logger.debug('Atom %s neither evaporate nor migrate nor drift' % (self.id))

def deposition(env):
    # create atom by DEPOSITION_RATE
    # TODO Currently not probability model for efficiency reason.
    logger = logging.getLogger(__name__)
    while True:
        try:
            yield env.timeout(1)
        except simpy.Interrupt as i:
            print('deposition process interrupted. ')
            return

        if Atom.num_atoms >= Config.SCOPE_SIZE * Config.SCOPE_SIZE * 2:
            logger.debug('Coverage 100% ')
            stop_process = env.process(stopSimulation())
            Context.addProcess('Stop', stop_process)
            # raise ValueError('Coverage 100%')
        deposition_rate = Config.DEPOSITION_RATE
        while deposition_rate >= 1:
            Atom.createAtom(env)
            deposition_rate -= 1
        if random.random() < deposition_rate:
            Atom.createAtom(env)

def clock(env):
    logger = logging.getLogger(__name__)
    start = time.clock()
    while True:
        logger.debug("clock: %d" % env.now)
        print("clock: %d / %s" % (env.now, Config.SIM_TIME))
        end = time.clock()
        if (end - start) > 60*Config.time_limit:
            # early termination
            print('simulation terminated due to long running time!')
            stop_process = env.process(stopSimulation())
            Context.addProcess('Stop', stop_process)

        try:
            yield env.timeout(1)
        except simpy.Interrupt as i:
            print('clock process interrupted. ')
            return


def configLogger(log_level, log_info_path):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # console handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    logger.addHandler(ch)

    # create a file handler
    fh = logging.FileHandler(log_info_path)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)

def printInfo(delta_mu):
    logger = logging.getLogger(__name__)
    now = datetime.datetime.now()
    logger.info(now.strftime("%Y-%m-%d %H:%M"))
    logger.info('Delta_Mu: %s' % (delta_mu))
    logger.info('Deposition rate per site: %s ' % Config.DEPOSITION_RATE_PER_SITE)
    logger.info("Simulation starts. #InitAtom: %d, Field: %d*%d, Time: %s" % (Config.NUM_ATOM, Config.SCOPE_SIZE, Config.SCOPE_SIZE, Config.SIM_TIME))

    print('Delta_Mu: %s' % (delta_mu))
    print('Deposition rate per site: %s ' % Config.DEPOSITION_RATE_PER_SITE)
    print("Simulation starts. #InitAtom: %d, Field: %d*%d, Time: %s" % (Config.NUM_ATOM, Config.SCOPE_SIZE, Config.SCOPE_SIZE, Config.SIM_TIME))

def cleanUp():
    logger = logging.getLogger(__name__)
    logger.handlers = []

def stopSimulation():
    # interrupt all other process
    while True:
        deposition_process = Context.getProcess('deposition')
        if deposition_process is not None:
            deposition_process.interrupt(('Stop', 0))
            yield deposition_process

        atoms = Context.getAtoms()
        for atom in atoms:
            atom.process.interrupt(('Stop', 0))

        clock_process = Context.getProcess('clock')
        if clock_process is not None:
            clock_process.interrupt(('Stop', 0))
            yield clock_process

        return

def main(delta_mu, repeat, log_level):
    log_info_path = 'logs/sim_deltamu%s%d' % (delta_mu, repeat)
    if os.path.exists(log_info_path):
        os.remove(log_info_path)

    configLogger(log_level, log_info_path)

    Config.setParameters(delta_mu)

    printInfo(delta_mu)

    if Config.SCOPE_SIZE * Config.SCOPE_SIZE * 2 < Config.NUM_ATOM:
        raise ValueError("Number of initial atom is too much")
    # Setup and start the simulation
    random.seed(Config.RANDOM_SEED)  # This helps reproducing the results
    # Create an environment and start the setup process
    env = simpy.Environment()

    field = Field(env, Config.SCOPE_SIZE)
    Atom.id = 0
    # Atom.field = field
    Atom.num_atoms = 0

    clock_process = env.process(clock(env))
    deposition_process = env.process(deposition(env))
    context = Context.create(field=field, env=env)
    context.addProcess('clock', clock_process)
    context.addProcess('deposition', deposition_process)
    Atom.createInitAtoms(env, Config.NUM_ATOM)
    # Execute!
    env.run(until=Config.SIM_TIME)

    cleanUp()

if __name__ == '__main__':


    main(1.5, 0, logging.DEBUG)