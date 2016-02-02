import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import copy
import numpy as np
from com.sirui.sim.position import Position
import shutil
import os
import logging
import sys
from itertools import islice

# TODO add growth rate v.s. driving potential plot

class LogParser(object):
    NUM_FRAME_SHOW = 20

    def __init__(self, beta_phi, beta_mu):
        self.beta_phi = beta_phi
        self.beta_mu = beta_mu
        self.fig_path = './images/sim_betaphi%s_betamu%s' % (self.beta_phi, self.beta_mu)
        self.log_path = './logs/sim_betaphi%s_betamu%s.log' % (self.beta_phi, self.beta_mu)
        self.frames = None

        # logger.setLevel(logging.INFO)
        logging.basicConfig(level=logging.DEBUG)
        # create a file handler
        handler = logging.FileHandler('log_parser.log')
        handler.setLevel(logging.INFO)

    # TODO improve efficiency, modify the figure instead of re plot
    def printFrames(self, frame_ids):
        logger = logging.getLogger(__name__)
        logger.info('Saving images... May take a while. ')
        fig = plt.figure()
        fig.hold(False)
        ax = fig.add_subplot(111)
        ax.hold(False)
        for id in frame_ids:
            (y, x) = np.nonzero(self.frames[id] != -1)
            ax.scatter(x, y)
            plt.savefig(self.fig_path + '/frame%d' % (id))
            # fig.clf()

    def main(self):
        logger = logging.getLogger(__name__)
        if os.path.exists(self.fig_path):
            logger.info('Cleaning images...' + self.fig_path)
            shutil.rmtree(self.fig_path)
        if not os.path.exists(self.fig_path):
            logger.info('Creating images folder... ' + self.fig_path)
            os.makedirs(self.fig_path)
        clock = 0
        atoms = []
        # TODO may need to buffer the lines if too large a file
        # TODO change parser. each line represent a variable
        with open(self.log_path, 'r') as f:
            timestamp = f.readline()
            para = f.readline()
            info = f.readline()
            words = info.split()
            # num_atom = int(words[3].strip()[:-1])
            l = len(words[5].strip())/2
            edge_size = int(words[5].strip()[:l-1])
            sim_time = int(words[7].strip())
            self.frames = np.full((sim_time, edge_size, edge_size), -1, np.int8)
            atoms = {} # atomId : position
            for line in islice(f, 2, None):
                if 'at' in line:
                    words = line.split()
                    new_clock = int(words[1].strip())
                    atomId = int(words[3].strip())
                    (a, b) = words[6].split(',')
                    new_position = Position(int(a[1:]), int(b[:-2]))
                    while clock < new_clock:
                        self.frames[clock+1] = copy.deepcopy(self.frames[clock])
                        clock += 1

                    old_position = atoms.get(atomId, None)
                    if old_position is not None:
                        self.frames[clock][old_position.x][old_position.y] = -1
                    self.frames[clock][new_position.x][new_position.y] = atomId
                    atoms[atomId] = new_position

                elif 'removed' in line:
                    words = line.split()
                    new_clock = int(words[1].strip())
                    atomId = int(words[3].strip())
                    (a, b) = words[7].split(',')
                    position = Position(int(a[1:]), int(b[:-2]))
                    while clock < new_clock:
                        self.frames[clock+1] = copy.deepcopy(self.frames[clock])
                        clock += 1

                    self.frames[clock][position.x][position.y] = -1
                    del atoms[atomId]

                else:
                    raise ValueError("Wrong line")

            while clock+1 < sim_time:
                self.frames[clock+1] = copy.deepcopy(self.frames[clock])
                clock += 1

        self.printFrames(range(0, clock, clock/LogParser.NUM_FRAME_SHOW))

if __name__ == '__main__':
    parser = LogParser(2.0, 2.0)
    parser.main()
