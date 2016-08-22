from __future__ import division

import matplotlib.pylab as plt
import numpy as np
from scipy.integrate import odeint

from model import f_rate_2
from config import Config

use_log_scale = True # fix

#####################################
c_ch4 = 20e-6
Config.setParameters(c_ch4)
y0 = [0, 0, 0, 0, 0, 0, 0]
####### High coverage zone ########
t = np.linspace(0, 60*30, 100000)
sol = odeint(f_rate_2, y0, t, mxstep=10000, atol=1e-8, rtol=1e-6)
# plot results
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.set_ylabel("Concentration (ML)", fontsize=20)
ax2.tick_params(axis='both', which='major', labelsize=10)
plt.xlabel('time ($min$)', fontsize=20)

t_min = np.divide(t, 60)
ax2.grid(True)
y = np.divide(sol, Config.n0)
if use_log_scale is True:
    ax2.set_ylim(ymin=1e-19, ymax=1)
    # concentration scales to ML
    ax2.loglog(t_min, y[:,1], 'r-', label='CH$_4$', linewidth=2)
    ax2.loglog(t_min, y[:,2], 'b-', label='CH$_x$', linewidth=2)
    ax2.loglog(t_min, y[:,3], 'g-', label='Unstable cluster', linewidth=2)
    ax2.loglog(t_min, y[:,4], 'k-', label='Stable cluster density', linewidth=2)
    ax2.loglog(t_min, y[:,5], 'c-', label='Stable cluster', linewidth=2)
    # ax2.loglog(t, sol[:, 5], 'y-', label='Defect-induced cluster area')
    # ax21.loglog(t, sol[:, 6], 'm--', label='Coverage')


ax2.legend(loc=0, prop={'size':14})
# if use_log_scale is True:
#     plt.savefig('solution_logscale.eps', format='eps', dpi=1000)
#     plt.savefig('/Users/raymon/Google Drive/UH/dissertation/dissertation/figure/chapter6/solution_logscale.eps', format='eps', dpi=1000)
#####################################
plt.show()

