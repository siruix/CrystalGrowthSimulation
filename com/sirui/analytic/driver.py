"""
Tuning parameters

"""

from com.sirui.analytic.log_parser import LogParser
import com.sirui.sim.TwoDSim as TwoDSim
import shutil
import os
beta_phi = [5.0, 7.0, 10.0]
# beta_phi = [5.0, 7.0, 10.0, 13.0, 15.0, 18.0, 20.0]
beta_delta_mu = [3.0, 5.0, 7.0]

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
            TwoDSim.main(x, y, i)
            parser = LogParser(x, y, i)
            parser.printFrames()