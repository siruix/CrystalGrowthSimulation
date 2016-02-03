"""
Tuning parameters

"""

from com.sirui.analytic.log_parser import LogParser
import com.sirui.sim.TwoDSim as TwoDSim
import shutil
import os

beta_phi = [0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
beta_delta_mu = [0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0]

print('Cleaning all previous logs and images...')
if os.path.exists('images'):
    shutil.rmtree('images')
if os.path.exists('logs'):
    shutil.rmtree('logs')
os.makedirs('images')
os.makedirs('logs')
for x in beta_phi:
    for y in beta_delta_mu:
        parser = LogParser(x, y, 10)
        for i in range(10):
            TwoDSim.main(x, y, i)
        parser.main()