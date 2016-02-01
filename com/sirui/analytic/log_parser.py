import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import copy
import numpy as np
from com.sirui.sim.position import Position
import shutil
import os
import logging

# TODO add growth rate v.s. driving potential plot

NUM_FRAME_SHOW = 20

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.DEBUG)

# create a file handler
handler = logging.FileHandler('log_parser.log')
handler.setLevel(logging.INFO)

# create a logging format
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


def getScatterPlotFormat(frame):
    return np.nonzero(frame != -1)

# TODO improve efficiency, modify the figure instead of re plot
def printFrames(frames, frame_ids):
    logger.info('Saving images... May take a while. ')
    fig = plt.figure()
    fig.hold(False)
    ax = fig.add_subplot(111)
    ax.hold(False)
    for id in frame_ids:
        (y, x) = getScatterPlotFormat(frames[id])
        ax.scatter(x, y)
        plt.savefig('./images/frame%d' % id)
        # fig.clf()

if __name__ == '__main__':
    if os.path.exists('images'):
        logger.info('Cleaning all previous images...')
        shutil.rmtree('images')
    if not os.path.exists('images'):
        logger.info('Creating images folder...')
        os.makedirs('images')
    frames = []
    clock = 0
    atoms = []
    # TODO may need to buffer the lines if too large a file
    # TODO change parser. each line represent a variable
    with open('../sim/info.log') as f:
        for line in f:
            if line.startswith('Simulation starts.'):
                words = line.split()
                num_atom = int(words[3].strip()[:-1])
                l = len(words[5].strip())/2
                edge_size = int(words[5].strip()[:l-1])
                sim_time = int(words[7].strip())
                # init frames with -1, meaning no atom
                # frames = [[[-1 for y in range(edge_size)] for x in range(edge_size)] for i in range(sim_time)]
                frames = np.full((sim_time, edge_size, edge_size), -1, np.int8)
                atoms = {} # atomId : position
            elif line.startswith('Clock'):
                if 'at' in line:
                    words = line.split()
                    new_clock = int(words[1].strip())
                    atomId = int(words[3].strip())
                    (a, b) = words[6].split(',')
                    new_position = Position(int(a[1:]), int(b[:-2]))
                    while clock < new_clock:
                        frames[clock+1] = copy.deepcopy(frames[clock])
                        clock += 1

                    old_position = atoms.get(atomId, None)
                    if old_position is not None:
                        frames[clock][old_position.x][old_position.y] = -1
                    frames[clock][new_position.x][new_position.y] = atomId
                    atoms[atomId] = new_position

                elif 'removed' in line:
                    words = line.split()
                    new_clock = int(words[1].strip())
                    atomId = int(words[3].strip())
                    (a, b) = words[7].split(',')
                    position = Position(int(a[1:]), int(b[:-2]))
                    while clock < new_clock:
                        frames[clock+1] = copy.deepcopy(frames[clock])
                        clock += 1

                    frames[clock][position.x][position.y] = -1
                    del atoms[atomId]

                else:
                    new_clock = -1
                    raise ValueError("Wrong line")



            else:
                pass

    printFrames(frames, range(0, clock, clock/NUM_FRAME_SHOW))


    pass