
from __future__ import division
import numpy as np
from com.sirui.sim.position import Position
from com.sirui.analytic.log_parser import LogParser

# VPython 3D display script

from visual import sphere
from visual import rate

atoms = {}
parser = LogParser(2.0, 2.0, 1)
motions = parser.getMotions()
for i in range(100):
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
                atoms[atom_id].pos = new_position.toCordinate()

    rate(1)