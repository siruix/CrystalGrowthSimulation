"""
Tuning parameters

"""
# TODO add defect points, improve nucleation
# TODO change model. beta_delta_mu match analytic model
from com.sirui.analytic.log_parser import LogParser
from com.sirui.sim.config import Config
import com.sirui.sim.simulate as sim
import shutil
import os
import logging


Config.time_limit = 10
Config.SIM_TIME = None
Config.Ea = 2.0
Config.T = 1000
concentration = [1e0, 1e1]

print('Cleaning all previous logs and images...')
if os.path.exists('logs'):
    shutil.rmtree('logs')
os.makedirs('logs')

for kn in concentration:
        for i in range(1):
            sim.main(kn, i, logging.WARNING)
