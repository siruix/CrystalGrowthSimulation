from __future__ import division

import matplotlib.pylab as plt
import numpy as np
from scipy.integrate import odeint

from model import *

# plot config
use_log_scale = False # fix this

c_ch4 = 30e-6
Config.setParameters(c_ch4)
y0 = [0, 0, 0, 0, 0, 1*Config.nd, 0]
# change sigma does not affect coverage dynamics.
sigma_1 = 1e-12
sigma = 1e-8
para = (sigma_1, sigma, sigma, sigma, Config.decay_rate)

t = np.linspace(0, 10, 10000)
sol = odeint(f_rate2, y0, t, args=(para,), mxstep=100000)
# plot results
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.set_ylabel("Concentration (ML)", fontsize=20)
ax2.tick_params(axis='both', which='major', labelsize=10)
plt.xlabel('time ($s$)', fontsize=20)

ax2.grid(True)

if use_log_scale is True:
    pass
else:
    # t_min = np.divide(t, 60)
    # ax2.plot(t_min, sol[:, 0], 'r-', label='CH4 count')
    y_adatom = np.divide(sol[:, 1], Config.n0)
    ax2.plot(t, y_adatom, 'b-', label='CH$_x$')
    # ax2.plot(t_min, sol[:, 2], 'g-', label='Meta-stable cluster count')
    # ax2.plot(t_min, sol[:, 3], 'k-', label='Stable cluster count')
    # ax2.plot(t_min, sol[:, 4], 'c-', label='Stable cluster area')
    # ax21.plot(t_min, sol[:, 5]/n0, 'y-', label='Defect-induced cluster area')
    # ax21.plot(coverage['5ppm'][0], coverage['5ppm'][1], 'ko', label='5ppm')
    # ax21.plot(coverage['10ppm'][0], coverage['10ppm'][1], 'ro', label='10ppm')
    # ax21.plot(coverage['20ppm'][0], coverage['20ppm'][1], 'bo', label='20ppm')
    # ax21.plot(coverage['30ppm'][0], coverage['30ppm'][1], 'co', label='30ppm')
    # ax21.plot(t_min, sol[:, 6], 'm-', label='Coverage')

ax2.legend(loc=0)

plt.savefig('adatom.eps', format='eps', dpi=1000)
plt.savefig('/Users/raymon/Google Drive/UH/dissertation/dissertation/figure/chapter6/adatom.eps', format='eps', dpi=1000)

#####################################
plt.show()

