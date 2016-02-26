from __future__ import division
# import copy
from com.sirui.sim.position import Position
# import os

class LogParser(object):

    def __init__(self, n, repeat = None):
        print('loading LogParser...')
        self.n = n
        if repeat is None:
            self.log_path = './logs/sim_kn%s' % (self.n)
        else:
            self.log_path = './logs/sim_kn%s%d' % (self.n, repeat)
        #
        # if not os.path.isdir('./frames'):
        #     os.makedirs('./frames')

        self.repeat = repeat
        self.motions = {}
        # Deposit   {clock : [(atom_id, 0, position)]}
        # Evaporate {clock : [(atom_id, 1, position)]}
        # Move      {clock : [(atom_id, 2, old_position, new_position)]}
        self.atoms = {}
        # self.coverage = None
        # self.growth_rate = None
        self.num_atom = 0
        self.deposition_rate_per_site = 0
        self.sim_time = None

        # create a file handler
        # fh = logging.FileHandler('log_parser.log')
        # fh.setLevel(logging.INFO)
        #
        # logger = logging.getLogger(__name__)
        # now = datetime.datetime.now()
        # logger.info(now.strftime("%Y-%m-%d %H:%M"))
        # if os.path.exists(self.frames_path):
        #     # logger.info('Cleaning frames file...' + self.frames_path)
        #     os.remove(self.frames_path)

        # parse the log file
        with open(self.log_path, 'r') as f:
            self.num_atom = 0
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
            if words[7].strip() == 'None':
                self.sim_time = None
            else:
                self.sim_time = int(words[7].strip())

            for line in f.readlines():
                if 'deposits' in line:
                    words = line.split()
                    clock = int(words[1].strip())
                    atomType = words[2].strip()
                    atomId = int(words[3].strip())
                    (a, b, c) = words[6].split(',')
                    position = Position(int(a[1:]), int(b), int(c[:-2]))
                    self.motions.setdefault(clock,[]).append( (atomType, atomId, 0, position) )

                elif 'evaporates' in line:
                    words = line.split()
                    clock = int(words[1].strip())
                    atomType = words[2].strip()
                    atomId = int(words[3].strip())
                    (a, b, c) = words[6].split(',')
                    position = Position(int(a[1:]), int(b), int(c[:-2]))
                    self.motions.setdefault(clock,[]).append( (atomType, atomId, 1, position) )

                elif 'moves' in line:
                    words = line.split()
                    clock = int(words[1].strip())
                    atomType = words[2].strip()
                    atomId = int(words[3].strip())
                    (a, b, c) = words[6].split(',')
                    old_position = Position(int(a[1:]), int(b), int(c[:-1]))
                    (a, b, c) = words[8].split(',')
                    new_position = Position(int(a[1:]), int(b), int(c[:-2]))
                    self.motions.setdefault(clock,[]).append( (atomType, atomId, 2, old_position, new_position) )

                else:
                    raise ValueError("Wrong line")

    # print frames data for external analytics
    # def printFrames(self):
    #     # logger = logging.getLogger(__name__)
    #     # logger.info('Saving frames... May take a while. ')
    #     # get full frames form motions
    #     frames = np.full((Config.SIM_TIME, Config.SCOPE_SIZE, Config.SCOPE_SIZE, 2), -1, np.int8)
    #
    #     for i in range(Config.SIM_TIME):
    #         if i != 0:
    #             frames[i] = copy.deepcopy(frames[i-1])
    #         motion_frame = self.motions.get(i)
    #         if motion_frame is not None:
    #             for move in motion_frame:
    #                 mode = move[1]
    #                 if mode == 0: # deposition
    #                     (atom_id, _, position) = move
    #                     frames[i][position.x][position.y][position.k] = atom_id
    #
    #                 elif mode == 1: # evaporation
    #                     (atom_id, _, position) = move
    #                     frames[i][position.x][position.y][position.k] = -1
    #
    #                 else: # migration
    #                     (atom_id, _, old_position, new_position) = move
    #                     frames[i][old_position.x][old_position.y][old_position.k] = -1
    #                     frames[i][new_position.x][new_position.y][new_position.k] = atom_id
    #         else:
    #             pass
    #
    #     with open(self.frames_path, 'w') as f:
    #         f.write(str(Config.SIM_TIME)+' ' + str(Config.SCOPE_SIZE) + ' ' + str(Config.SCOPE_SIZE) + '\n')
    #         f.write(str(self.deposition_rate_per_site)+'\n')
    #         for i in range(Config.SIM_TIME):
    #             for j in range(Config.SCOPE_SIZE):
    #                 for k in range(Config.SCOPE_SIZE):
    #                     f.write('%s ' % frames[i][j][k][0])
    #                     f.write('%s ' % frames[i][j][k][1])
    #             f.write('\n')

    def getMotions(self):
        return self.motions


if __name__ == '__main__':
    parser = LogParser(2.0, 1)
    # parser.printFrames()
