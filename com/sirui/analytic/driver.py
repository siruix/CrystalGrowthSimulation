"""
Tuning parameters

"""

from com.sirui.analytic.log_parser import LogParser
import com.sirui.sim.TwoDSim as TwoDSim
import shutil
import os
import logging
beta_phi = [0.2, 0.5]
# beta_phi = [5.0, 7.0, 10.0, 13.0, 15.0, 18.0, 20.0]
beta_delta_mu = [0.1]

print('Cleaning all previous logs and images...')
if os.path.exists('images'):
    shutil.rmtree('images')
if os.path.exists('logs'):
    shutil.rmtree('logs')
os.makedirs('images')
os.makedirs('logs')
for x in beta_phi:
    for y in beta_delta_mu:
        for i in range(1):
            TwoDSim.main(x, y, i, logging.INFO)
            parser = LogParser(x, y, i)
            parser.printFrames()