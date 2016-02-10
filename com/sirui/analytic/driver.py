"""
Tuning parameters

"""

from com.sirui.analytic.log_parser import LogParser
import com.sirui.sim.TwoDSim as TwoDSim
import shutil
import os
import logging
beta_phi =      [1.5, 1.5]
beta_delta_mu = [0.3, 0.4]

print('Cleaning all previous logs and images...')
if os.path.exists('images'):
    shutil.rmtree('images')
if os.path.exists('logs'):
    shutil.rmtree('logs')
os.makedirs('images')
os.makedirs('logs')
for x,y in zip(beta_phi, beta_delta_mu):
        for i in range(1):
            TwoDSim.main(x, y, i, logging.WARNING)
            # parser = LogParser(x, y, i)
            # parser.printFrames()