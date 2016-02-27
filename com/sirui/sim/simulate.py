from __future__ import print_function
import os
import datetime
import time
from com.sirui.sim.resources import *
from com.sirui.sim.atom import *

def adsorption():
    logger = logging.getLogger()
    while True:
        try:
            yield Context.getEnv().timeout(1)
        except simpy.Interrupt as i:
            print('adsorption process interrupted. ')
            return

        if Atom.num >= Config.SCOPE_SIZE * Config.SCOPE_SIZE * Config.SCOPE_HEIGHT:
            logger.debug('reaches 100% ')
            stop_process = Context.getEnv().process(stopSimulation())
            Context.addProcess('Stop', stop_process)

        adsorption_rate = Config.ADSORPTION_RATE
        while adsorption_rate >= 1:
            Atom.createOne()
            adsorption_rate -= 1
        if random.random() < adsorption_rate:
            Atom.createOne()

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




def printInfo():
    logger = logging.getLogger()
    now = datetime.datetime.now()
    logger.info(now.strftime("%Y-%m-%d %H:%M"))
    logger.info('Delta_Mu: %s Phi: %s' % (Config.delta_mu, Config.phi))
    logger.info('Deposition rate per site: %s ' % Config.ADSORPTION_RATE_PER_SITE)
    logger.info("Simulation starts. #InitAtom: %d, Field: %d*%d*%d, Time: %s" % (Config.NUM_ATOM, Config.SCOPE_SIZE, Config.SCOPE_SIZE, Config.SCOPE_HEIGHT, Config.SIM_TIME))

    print('Delta_Mu: %s Phi: %s' % (Config.delta_mu, Config.phi))
    print('Deposition rate per site: %s ' % Config.ADSORPTION_RATE_PER_SITE)
    print("Simulation starts. #InitAtom: %d, Field: %d*%d*%d, Time: %s" % (Config.NUM_ATOM, Config.SCOPE_SIZE, Config.SCOPE_SIZE, Config.SCOPE_HEIGHT, Config.SIM_TIME))

def cleanUp():
    logger = logging.getLogger()
    logger.handlers = []

def stopSimulation():
    # interrupt all other process
    while True:
        deposition_process = Context.getProcess('Adsorption')
        if deposition_process is not None:
            deposition_process.interrupt(('Stop', 0))
            yield deposition_process

        atoms = Context.getAtoms()
        for atom in atoms:
            atom.process.interrupt(('Stop', 0))

        clock_process = Context.getProcess('Clock')
        if clock_process is not None:
            clock_process.interrupt(('Stop', 0))
            yield clock_process

        return

def resetAtoms():
    Atom.id = 0
    Atom.num = 0

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

def main(delta_mu, phi, log_level):
    log_info_path = 'logs/sim_mu%s_phi%s' % (delta_mu, phi)
    if os.path.exists(log_info_path):
        os.remove(log_info_path)

    configLogger(log_level, log_info_path)

    Config.setParameters(delta_mu, phi)

    printInfo()

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
    deposition_process = env.process(adsorption())

    context.addProcess('Clock', clock_process)
    context.addProcess('Adsorption', deposition_process)
    Atom.createInit(Config.NUM_ATOM)

    # Execute!
    env.run(until=Config.SIM_TIME)

    cleanUp()

if __name__ == '__main__':


    main(1.0, 0.1, logging.DEBUG)