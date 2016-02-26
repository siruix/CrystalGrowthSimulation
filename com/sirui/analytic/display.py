
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
kn = 1e1
parser = LogParser(kn, 0)
motions = parser.getMotions()
for i in range(len(motions)):
    motion_frame = motions.get(i)
    if motion_frame is not None:
        for move in motion_frame:
            mode = move[2]
            if mode == 0:
                (atomType, atom_id, _, position) = move
                atoms.setdefault((atomType, atom_id), sphere(pos = position.toCoordinate(), radius = 0.3))
            elif mode == 1:
                (atomType, atom_id, _, position) = move
                # remove sphere
                atoms[(atomType, atom_id)].visible = False
            else:
                (atomType, atom_id, _, old_position, new_position) = move
                atoms[(atomType, atom_id)].pos = new_position.toCoordinate()

    rate(50)