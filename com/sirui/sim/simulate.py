from __future__ import print_function
import logging
import logging.config
import os
import datetime
import time
from com.sirui.sim.resources import *
from com.sirui.sim.context import *
from com.sirui.sim.config import Config
from com.sirui.sim.position import Position
from com.sirui.sim.utility import *
from com.sirui.sim.atom import *
import numpy as np

def deposition():
    # create Carbon by DEPOSITION_RATE
    # Do not create Defect
    # TODO Currently not exact probability model for efficiency reason.
    logger = logging.getLogger()
    while True:
        try:
            yield Context.getEnv().timeout(1)
        except simpy.Interrupt as i:
            print('deposition process interrupted. ')
            return

        if Carbon.num >= Config.SCOPE_SIZE * Config.SCOPE_SIZE * 2:
            logger.debug('Coverage 100% ')
            stop_process = Context.getEnv().process(stopSimulation())
            Context.addProcess('Stop', stop_process)

        deposition_rate = Config.DEPOSITION_RATE
        while deposition_rate >= 1:
            Carbon.createOne()
            deposition_rate -= 1
        if random.random() < deposition_rate:
            Carbon.createOne()

def clock():
    logger = logging.getLogger()
    start = time.clock()
    while True:
        logger.debug("clock: %d" % Context.getEnv().now)
        end = time.clock()
        print("clock: %d / %s. %d%%" % (Context.getEnv().now, Config.SIM_TIME, round((end - start)*100/60/Config.time_limit)))
        if (end - start) > 60*Config.time_limit:
            # early termination
            print('simulation terminated due to long running time!')
            stop_process = Context.getEnv().process(stopSimulation())
            Context.addProcess('Stop', stop_process)

        try:
            yield Context.getEnv().timeout(1)
        except simpy.Interrupt as i:
            print('clock process interrupted. ')
            return




def printInfo(delta_mu):
    logger = logging.getLogger()
    now = datetime.datetime.now()
    logger.info(now.strftime("%Y-%m-%d %H:%M"))
    logger.info('Delta_Mu: %s' % (delta_mu))
    logger.info('Deposition rate per site: %s ' % Config.DEPOSITION_RATE_PER_SITE)
    logger.info("Simulation starts. #InitAtom: %d, Field: %d*%d, Time: %s" % (Config.NUM_ATOM, Config.SCOPE_SIZE, Config.SCOPE_SIZE, Config.SIM_TIME))

    print('Delta_Mu: %s' % (delta_mu))
    print('Deposition rate per site: %s ' % Config.DEPOSITION_RATE_PER_SITE)
    print("Simulation starts. #InitAtom: %d, Field: %d*%d, Time: %s" % (Config.NUM_ATOM, Config.SCOPE_SIZE, Config.SCOPE_SIZE, Config.SIM_TIME))

def cleanUp():
    logger = logging.getLogger()
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

def getDefectPositions():
    # assume defect cluster are the 3 rings around defect point
    defect_points = []
    x = np.rint(np.linspace(0, Config.SCOPE_SIZE, Config.NUM_DEFECT+2))
    y = np.rint(np.linspace(0, Config.SCOPE_SIZE, Config.NUM_DEFECT+2))
    xv,yv = np.meshgrid(x[1:-1], y[1:-1])
    for i in range(Config.NUM_DEFECT):
        for j in range(Config.NUM_DEFECT):
            defect_points.append(Position(xv[i,j], yv[i,j], 0))
            defect_points.append(Position(xv[i,j], yv[i,j], 1))

            defect_points.append(Position(xv[i,j]+1, yv[i,j], 0))

            defect_points.append(Position(xv[i,j]-1, yv[i,j], 0))
            defect_points.append(Position(xv[i,j]-1, yv[i,j], 1))

            defect_points.append(Position(xv[i,j], yv[i,j]+1, 0))
            defect_points.append(Position(xv[i,j], yv[i,j]+1, 1))

            defect_points.append(Position(xv[i,j], yv[i,j]-1, 0))
            defect_points.append(Position(xv[i,j], yv[i,j]-1, 1))

            defect_points.append(Position(xv[i,j]-1, yv[i,j]+1, 0))
            defect_points.append(Position(xv[i,j]-1, yv[i,j]+1, 1))

            defect_points.append(Position(xv[i,j]+1, yv[i,j]-1, 0))

            defect_points.append(Position(xv[i,j]-2, yv[i,j]+1, 1))

    Config.DEFECT_POSITIONS = defect_points
    return defect_points

def resetAtoms():
    Carbon.id = 0
    Carbon.num = 0
    Defect.id = 0
    Defect.num = 0

def configLogger(log_level, log_info_path):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # console handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    logger.addHandler(ch)

    # create a file handler
    fh = logging.FileHandler(log_info_path)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)

def main(kn, repeat, log_level):
    log_info_path = 'logs/sim_kn%s%d' % (kn, repeat)
    if os.path.exists(log_info_path):
        os.remove(log_info_path)

    configLogger(log_level, log_info_path)

    Config.setParameters(kn)

    printInfo(kn)

    if Config.SCOPE_SIZE * Config.SCOPE_SIZE * 2 < Config.NUM_ATOM:
        raise ValueError("Number of initial atom is too much")
    # Setup and start the simulation
    random.seed(Config.RANDOM_SEED)  # This helps reproducing the results
    # Create an environment and start the setup process
    env = simpy.Environment()
    field = Field(env, Config.SCOPE_SIZE)
    context = Context.create(field=field, env=env)
    resetAtoms()

    clock_process = env.process(clock())
    deposition_process = env.process(deposition())

    context.addProcess('clock', clock_process)
    context.addProcess('deposition', deposition_process)
    Defect.createInit(getDefectPositions())
    Carbon.createInit(Config.NUM_ATOM)

    # Execute!
    env.run(until=Config.SIM_TIME)

    cleanUp()

if __name__ == '__main__':


    main(1.5, 0, logging.DEBUG)