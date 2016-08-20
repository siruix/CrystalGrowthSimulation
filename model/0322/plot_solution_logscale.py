from __future__ import division

import matplotlib.pylab as plt
import numpy as np
from scipy.integrate import odeint

from model import *

# plot config
use_log_scale = True # fix

#####################################
c_ch4 = 30e-6
Config.setParameters(c_ch4)
y0 = [0, 0, 0, 0, 0, 1*Config.nd, 0]
# change sigma does not affect coverage dynamics.
sigma_1 = 1e-12
sigma = 1e-8
para = (sigma_1, sigma, sigma, sigma, Config.decay_rate)

####### High coverage zone ########
t = np.linspace(0, 60*30, 10000)
sol = odeint(f_rate2, y0, t, args=(para,), mxstep=100000)
# plot results
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.set_ylabel("Concentration (ML)", fontsize=20)
ax2.tick_params(axis='both', which='major', labelsize=10)
plt.xlabel('time ($min$)', fontsize=20)
ax21 = ax2.twinx()
ax21.set_ylabel("Coverage (ML)", fontsize=20)
ax21.tick_params(axis='both', which='major', labelsize=10)

ax2.grid(True)

if use_log_scale is True:
    ax2.set_ylim(ymin=1e-19, ymax=1)
    # concentration scales to ML
    ax2.loglog(t, np.divide(sol[:, 0], Config.n0), 'r-', label='CH$_4$', linewidth=2)
    ax2.loglog(t, np.divide(sol[:, 1], Config.n0), 'b-', label='CH$_x$', linewidth=2)
    ax2.loglog(t, np.divide(sol[:, 2], Config.n0), 'g-', label='Unstable cluster', linewidth=2)
    # ax2.loglog(t, sol[:, 3], 'k-', label='Stable cluster')
    ax2.loglog(t, np.divide(sol[:, 4], Config.n0), 'c-', label='Stable cluster', linewidth=2)
    # ax2.loglog(t, sol[:, 5], 'y-', label='Defect-induced cluster area')
    # ax21.loglog(t, sol[:, 6], 'm--', label='Coverage')


ax2.legend(loc=4, prop={'size':18})
ax21.legend(loc=0)
if use_log_scale is True:
    plt.savefig('solution_logscale.eps', format='eps', dpi=1000)
    plt.savefig('/Users/raymon/Google Drive/UH/dissertation/dissertation/figure/chapter6/solution_logscale.eps', format='eps', dpi=1000)
#####################################
plt.show()

