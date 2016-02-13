"""
Tuning parameters

"""
# TODO add defect points, improve nucleation
# TODO change model. beta_delta_mu match analytic model
from com.sirui.analytic.log_parser import LogParser
from com.sirui.sim.config import Config
import com.sirui.sim.TwoDSim as TwoDSim
import shutil
import os
import logging

delta_mu = [0.0]
Config.time_limit = 20
Config.SIM_TIME = None
print('Cleaning all previous logs and images...')
if os.path.exists('logs'):
    shutil.rmtree('logs')
os.makedirs('logs')

for x in delta_mu:
        for i in range(1):
            TwoDSim.main(x, i, logging.WARNING)
