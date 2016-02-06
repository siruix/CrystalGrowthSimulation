from __future__ import division
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import copy
import numpy as np
from com.sirui.sim.position import Position
import shutil
import os
import logging
import datetime
from itertools import islice
from com.sirui.sim.config import Config


# TODO add growth rate v.s. driving potential plot

class LogParser(object):
    NUM_FRAME_SHOW = 20

    def __init__(self, beta_phi, beta_mu, repeat):
        self.beta_phi = beta_phi
        self.beta_mu = beta_mu
        self.fig_path = './images/sim_betaphi%s_betamu%s' % (self.beta_phi, self.beta_mu)
        self.log_path = './logs/sim_betaphi%s_betamu%s' % (self.beta_phi, self.beta_mu)
        self.motions = {}
        # Deposit   {clock : [(atom_id, 0, position)]}
        # Evaporate {clock : [(atom_id, 1, position)]}
        # Move      {clock : [(atom_id, 2, old_position, new_position)]}
        self.atoms = {}
        self.coverage = None
        self.growth_rate = None
        self.num_atom = 0
        self.repeat = repeat
        self.deposition_rate_per_site = 0
        # logger.setLevel(logging.INFO)
        logging.basicConfig(level=logging.DEBUG)
        # create a file handler
        handler = logging.FileHandler('log_parser.log')
        handler.setLevel(logging.INFO)

        logger = logging.getLogger(__name__)
        now = datetime.datetime.now()
        logger.info(now.strftime("%Y-%m-%d %H:%M"))
        if os.path.exists(self.fig_path):
            logger.info('Cleaning images...' + self.fig_path)
            shutil.rmtree(self.fig_path)
        if not os.path.exists(self.fig_path):
            logger.info('Creating images folder... ' + self.fig_path)
            os.makedirs(self.fig_path)

        # TODO may need to buffer the lines if too large a file
        # TODO change parser. each line represent a variable
        for i in range(self.repeat):
            with open(self.log_path + '%d' % i, 'r') as f:
                self.num_atom = 0
                clock = 0
                timestamp = f.readline()
                para = f.readline()
                deposition_rate_info = f.readline()
                words = deposition_rate_info.split()
                self.deposition_rate_per_site = float(words[4])
                info = f.readline()
                words = info.split()
                # num_atom = int(words[3].strip()[:-1])
                l = len(words[5].strip())//2
                edge_size = int(words[5].strip()[:l-1])
                sim_time = int(words[7].strip())
                # self.frames = np.full((sim_time, edge_size, edge_size, 2), -1, np.int8)
                # self.atoms = {} # atomId : position
                coverage = np.zeros(sim_time)

                for line in f.readlines():
                    if 'deposits' in line:
                        words = line.split()
                        clock = int(words[1].strip())
                        atomId = int(words[3].strip())
                        (a, b, c) = words[6].split(',')
                        position = Position(int(a[1:]), int(b), int(c[:-2]))
                        # while clock < new_clock:
                        #     self.frames[clock+1] = copy.deepcopy(self.frames[clock])
                        #     coverage[clock] = self.num_atom / edge_size / edge_size / 2
                        #     clock += 1
                        self.motions.setdefault(clock,[]).append( (atomId, 0, position) )
                        # old_position = self.atoms.get(atomId, None)
                        # if old_position is not None:
                        #     self.frames[clock][old_position.x][old_position.y][old_position.k] = -1
                        #     self.num_atom -= 1
                        # self.frames[clock][new_position.x][new_position.y][new_position.k] = atomId
                        # self.atoms[atomId] = new_position
                        # self.num_atom += 1
                    elif 'evaporates' in line:
                        words = line.split()
                        clock = int(words[1].strip())
                        atomId = int(words[3].strip())
                        (a, b, c) = words[6].split(',')
                        position = Position(int(a[1:]), int(b), int(c[:-2]))
                        self.motions.setdefault(clock,[]).append( (atomId, 1, position) )

                    elif 'moves' in line:
                        words = line.split()
                        clock = int(words[1].strip())
                        atomId = int(words[3].strip())
                        (a, b, c) = words[6].split(',')
                        old_position = Position(int(a[1:]), int(b), int(c[:-2]))
                        (a, b, c) = words[8].split(',')
                        new_position = Position(int(a[1:]), int(b), int(c[:-2]))
                        self.motions.setdefault(clock,[]).append( (atomId, 2, old_position, new_position) )
                        # while clock < new_clock:
                        #     self.frames[clock+1] = copy.deepcopy(self.frames[clock])
                        #     coverage[clock] = self.num_atom / edge_size / edge_size / 2
                        #     clock += 1
                        #
                        #
                        # self.frames[clock][position.x][position.y][position.k] = -1
                        # del self.atoms[atomId]
                        # self.num_atom -= 1

                    else:
                        raise ValueError("Wrong line")

    # TODO Draw graphene lattice figure
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

    def printRate(self):
        #TODO Rate = R / k_plus
        self.growth_rate = np.diff(self.coverage)
        fig = plt.figure()
        fig.hold(False)
        ax = fig.add_subplot(111)
        ax.hold(False)
        ax.plot(self.coverage[:-1], self.growth_rate, 'ro')
        plt.savefig(self.fig_path + '/rate_coverage')
        ax.plot(range(len(self.coverage)), self.coverage, 'ro')
        plt.savefig(self.fig_path + '/coverage_time')
        np.savetxt(self.fig_path + "/coverage.csv", self.coverage, delimiter=",")
        with open(self.fig_path + "/deposition_rate_per_site.txt", 'w') as f:
            f.write('%s'% self.deposition_rate_per_site)
        plt.close('all')

    def getMotions(self):
        return self.motions


    def main(self):
        pass

        #         coverage[clock] = self.num_atom / edge_size / edge_size / 2
        #         while clock+1 < sim_time:
        #             self.frames[clock+1] = copy.deepcopy(self.frames[clock])
        #             clock += 1
        #             coverage[clock] = self.num_atom / edge_size / edge_size / 2
        #     if self.coverage is None:
        #         self.coverage = coverage
        #     else:
        #         self.coverage += coverage
        # self.coverage /= self.repeat
        # # self.printFrames(range(0, clock, clock//LogParser.NUM_FRAME_SHOW))
        # self.printRate()

if __name__ == '__main__':
    parser = LogParser(2.0, 2.0, 1)
    # parser.main()
