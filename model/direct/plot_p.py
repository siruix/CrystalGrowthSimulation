from __future__ import division

import matplotlib.pylab as plt
import numpy as np
from cycler import cycler
from scipy.integrate import odeint

from  model.direct.model_i2_defect import *

####
# E_des = 0.15
# E_diff = 0.1
# A_const = 7e11
# B_const = 1e-2
# delta_E_decay = 0.4
#####################################
# Experimental data Ref: Wu. Two-step growth
coverage = {}
coverage['30ppm'] = ([0, 5, 10, 15, 20], [0, 0.78, 0.97, 0.99, 1])
coverage['20ppm'] = ([0, 5, 10, 15, 20, 25, 30], [0, 0.58, 0.83, 0.94, 0.96, 0.99, 1])
coverage['10ppm'] = ([0, 5, 10, 15, 20, 25, 30, 60], [0, 0.19, 0.38, 0.57, 0.75, 0.86, 0.94, 0.99])
coverage['5ppm'] = ([0, 5, 10, 15, 20, 25, 30, 60], [0, 0.03, 0.15, 0.22, 0.33, 0.38, 0.48, 0.7])

######################################
t = np.linspace(0, 60*60, 10000)
y0 = [0, 0, 0, 0, 0, 1*Config.nd, 0]
sigma = 1e-12
para = (sigma, sigma, sigma, sigma, Config.decay_rate)
c_ch4 = [30e-6, 20e-6, 10e-6, 5e-6]
# c_ch4 = [30e-6]
sol = []
for c in c_ch4:
    Config.set_parameters(c)
    sol.append( odeint(f_rate2, y0, t, args=(para,), mxstep=100000) )
# plot results
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_prop_cycle(cycler('color', ['c', 'b', 'r', 'k']))
plt.xlabel('t/min')
# plt.title('coverage v.s. time')
ax.set_ylabel("Coverage")
t_min = np.divide(t, 60)
ax.plot(coverage['30ppm'][0], coverage['30ppm'][1], 'o', label='30ppm')
ax.plot(coverage['20ppm'][0], coverage['20ppm'][1], 'o', label='20ppm')
ax.plot(coverage['10ppm'][0], coverage['10ppm'][1], 'o', label='10ppm')
ax.plot(coverage['5ppm'][0], coverage['5ppm'][1], 'o', label='5ppm')
for y in sol:
    ax.plot(t_min, y[:, 6], '-')

ax.legend(loc=0)
#####################################

plt.show()

