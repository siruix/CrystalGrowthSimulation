from __future__ import division

import matplotlib.pylab as plt
import numpy as np
from cycler import cycler
from scipy.integrate import odeint

from model import f_rate_2
from config import Config

####
# E_des = 0.15
# E_diff = 0.1
# A_const = 7e11
# B_const = 1e-2
# delta_E_decay = 0.4
#####################################
# Experimental data Ref: Xing. Kinetic.
time = [0, 5, 10, 15, 20, 30, 60]
coverage = {}
coverage['1050'] = (time, [0, 0.5718, 0.824, 0.9665, 0.9862, 1, 1])
coverage['1025'] = (time, [0, 0.4875, 0.6845, 0.8752, 0.9342, 0.9912, 1])
coverage['1000'] = (time, [0, 0.172, 0.5307, 0.6911, 0.817, 0.8735, 0.9897])
coverage['950'] =  (time, [0, 0.1085, 0.2629, 0.4527, 0.5409, 0.6104, 0.8266])
coverage['900'] =  (time, [0, 0.072, 0.1208, 0.131, 0.1382, 0.1942, 0.3542])
######################################
t = np.linspace(0, 60*60, 10000)
y0 = [0, 0, 0, 0, 0, 0, 0]
c_ch4 = 20e-6
Temperature = [1050, 1025, 1000, 950, 900] # in C
sol = []
for T in Temperature:
    Config.setParameters(c_ch4, T + 273 + 50)
    sol.append( odeint(f_rate_2, y0, t, mxstep=10000, atol=1e-8, rtol=1e-6) )
# plot results
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle(cycler('color', ['r', 'g', 'b', 'm', 'k']))
ax.tick_params(axis='both', which='major', labelsize=15)
plt.xlabel('time ($min$)', fontsize=20)
ax.set_ylabel("Graphene Coverage (ML)", fontsize=20)
t_min = np.divide(t, 60)
ax.plot(coverage['1050'][0], coverage['1050'][1], 'o', label='1050$^\circ$C')
ax.plot(coverage['1025'][0], coverage['1025'][1], 'o', label='1025$^\circ$C')
ax.plot(coverage['1000'][0], coverage['1000'][1], 'o', label='1000$^\circ$C')
ax.plot(coverage['950'][0], coverage['950'][1], 'o', label='950$^\circ$C')
ax.plot(coverage['900'][0], coverage['900'][1], 'o', label='900$^\circ$C')
for y in sol:
    ax.plot(t_min, y[:, 0], '-')

ax.legend(loc=0, numpoints=1, fontsize=15)
ax.grid(True)
#####################################
# plt.savefig('temperature_effect.eps', format='eps', dpi=1000)
# plt.savefig('/Users/raymon/Google Drive/UH/dissertation/dissertation/figure/chapter6/temperature_effect.eps', format='eps', dpi=1000)
plt.show()

