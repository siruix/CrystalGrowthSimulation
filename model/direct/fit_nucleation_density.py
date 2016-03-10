from __future__ import division

import matplotlib.pylab as plt
import numpy as np
from cycler import cycler
from scipy.integrate import odeint

from  model.direct.model_i2_defect import *

#####################################
# Experimental data Ref: Wu. Two-step growth
coverage = {}
coverage['30ppm'] = ([0, 5, 10, 15, 20], [0, 0.78, 0.97, 0.99, 1])
coverage['20ppm'] = ([0, 5, 10, 15, 20, 25, 30], [0, 0.58, 0.83, 0.94, 0.96, 0.99, 1])
coverage['10ppm'] = ([0, 5, 10, 15, 20, 25, 30, 60], [0, 0.19, 0.38, 0.57, 0.75, 0.86, 0.94, 0.99])
coverage['5ppm'] = ([0, 5, 10, 15, 20, 25, 30, 60], [0, 0.03, 0.15, 0.22, 0.33, 0.38, 0.48, 0.7])
# nucleation density for CH4 5ppm, 10ppm, 20ppm, 30ppm
nucleation_density = [3.4e5, 3.95e5, 4.4e5, 5.8e5]
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
ax.set_xlabel('t/min')
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

##########
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.set_prop_cycle(cycler('color', ['c', 'b', 'r', 'k']))
ax2.plot([5, 10, 20, 30], nucleation_density, 'o', label='Experiment')
n = []
for y in sol:
    n.append(y[-len(y[:,3])*0.9, 3])
ax2.plot([30, 20, 10, 5], n, 'o', label='Model')
ax2.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax2.set_xticks(np.arange(0, 40, 5))
ax2.set_xlabel('Methane partial pressure (ppm)')
ax2.set_ylabel('Nucleation density (#/cm2)')
ax2.grid(True)
ax2.legend(loc=0)
#####################################

plt.show()

