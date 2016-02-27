
from __future__ import division
from com.sirui.analytic.log_parser import LogParser
from com.sirui.sim.config import Config
# VPython 3D display script

from visual import sphere
from visual import rate
from visual import display
from math import sqrt
scene = display(center = (Config.SCOPE_SIZE/2, Config.SCOPE_SIZE/2, Config.SCOPE_HEIGHT/2))

atoms = {}
delta_mu = 1.0
phi = 1.0

parser = LogParser(delta_mu, phi)
motions = parser.getMotions()
for i in range(len(motions)):
    motion_frame = motions.get(i)
    if motion_frame is not None:
        for move in motion_frame:
            mode = move[2]
            if mode == 0:
                (atomType, atom_id, _, position) = move
                atoms.setdefault((atomType, atom_id), sphere(pos = position.toCoordinate(), radius = 0.5))
            elif mode == 1:
                (atomType, atom_id, _, position) = move
                # remove sphere
                atoms[(atomType, atom_id)].visible = False
            else:
                (atomType, atom_id, _, old_position, new_position) = move
                atoms[(atomType, atom_id)].pos = new_position.toCoordinate()

    rate(15)