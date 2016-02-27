from __future__ import division
# import copy
from com.sirui.sim.position import Position
# import os

class LogParser(object):

    def __init__(self, delta_mu, phi):
        print('loading LogParser...')
        self.delta_mu = delta_mu
        self.phi = phi
        self.log_path = './logs/sim_mu%s_phi%s' % (self.delta_mu, self.phi)
        self.motions = {}
        # Deposit   {clock : [(atom_id, 0, position)]}
        # Evaporate {clock : [(atom_id, 1, position)]}
        self.atoms = {}
        self.num_atom = 0
        self.deposition_rate_per_site = 0
        self.sim_time = None

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
            dimensions = words[5][:-1].split('*')
            x = int(dimensions[0])
            y = int(dimensions[1])
            z = int(dimensions[2])
            edge_size = x
            if words[7].strip() == 'None':
                self.sim_time = None
            else:
                self.sim_time = int(words[7].strip())

            for line in f.readlines():
                if 'adsorb' in line:
                    words = line.split()
                    clock = int(words[1].strip())
                    atomType = words[2].strip()
                    atomId = int(words[3].strip())
                    (a, b, c) = words[6].split(',')
                    position = Position(int(a[1:]), int(b), int(c[:-2]))
                    self.motions.setdefault(clock,[]).append( (atomType, atomId, 0, position) )

                elif 'desorb' in line:
                    words = line.split()
                    clock = int(words[1].strip())
                    atomType = words[2].strip()
                    atomId = int(words[3].strip())
                    (a, b, c) = words[6].split(',')
                    position = Position(int(a[1:]), int(b), int(c[:-2]))
                    self.motions.setdefault(clock,[]).append( (atomType, atomId, 1, position) )

                elif 'diffuse' in line:
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

    def getMotions(self):
        return self.motions


if __name__ == '__main__':
    parser = LogParser(0.1, 2.0)
