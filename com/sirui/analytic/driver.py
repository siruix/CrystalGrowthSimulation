"""
Tuning parameters

"""

from com.sirui.analytic.log_parser import LogParser
import com.sirui.sim.TwoDSim as TwoDSim
import shutil
import os

beta_phi = [1.0, 2.0, 5.0]
beta_delta_mu = [1.0, 2.0, 5.0]

print('Cleaning all previous logs and images...')
if os.path.exists('images'):
    shutil.rmtree('images')
if os.path.exists('logs'):
    shutil.rmtree('logs')
os.makedirs('images')
os.makedirs('logs')
for x in beta_phi:
    for y in beta_delta_mu:
        TwoDSim.main(x, y)
        parser = LogParser(x, y)
        parser.main()