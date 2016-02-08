
from __future__ import division
from com.sirui.analytic.log_parser import LogParser
from com.sirui.sim.config import Config
# VPython 3D display script

from visual import sphere
from visual import rate
from visual import display
from math import sqrt
# self.x + 0.5 * self.y, self.y * sqrt(3) / 2
scene = display(center = (Config.SCOPE_SIZE/2 * 1.5, Config.SCOPE_SIZE/2 * sqrt(3)/2, 0))

atoms = {}
beta_phi = 0.5
beta_delta_mu = 0.1
parser = LogParser(beta_phi, beta_delta_mu, 0)
motions = parser.getMotions()
for i in range(Config.SIM_TIME):
    motion_frame = motions.get(i)
    if motion_frame is not None:
        for move in motion_frame:
            mode = move[1]
            if mode == 0:
                (atom_id, _, position) = move
                atoms.setdefault(atom_id, sphere(pos = position.toCoordinate(), radius = 0.3))
            elif mode == 1:
                (atom_id, _, position) = move
                # remove sphere
                atoms[atom_id].visible = False
            else:
                (atom_id, _, old_position, new_position) = move
                atoms[atom_id].pos = new_position.toCoordinate()

    rate(1)