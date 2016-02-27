from com.sirui.sim.config import Config
import com.sirui.sim.simulate as sim
import shutil
import os
import logging

Config.time_limit = 10
Config.SIM_TIME = None
Config.SCOPE_HEIGHT = 30
delta_mu = [1.0, 2.0]
phi = [1.0, 1.5, 2.0, 2.5]

print('Cleaning all previous logs and images...')
if os.path.exists('logs'):
    shutil.rmtree('logs')
os.makedirs('logs')

for y in phi:
    for x in delta_mu:
        sim.main(x, y, logging.WARNING)
