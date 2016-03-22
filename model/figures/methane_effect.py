import matplotlib.pylab as plt
import numpy as np
from cycler import cycler
#####################################
# Experimental data Ref: Wu. Two-step growth
coverage = {}
coverage['30ppm'] = ([0, 5, 10, 15, 20], [0, 0.78, 0.97, 0.99, 1])
coverage['20ppm'] = ([0, 5, 10, 15, 20, 25, 30], [0, 0.58, 0.83, 0.94, 0.96, 0.99, 1])
coverage['10ppm'] = ([0, 5, 10, 15, 20, 25, 30, 60], [0, 0.19, 0.38, 0.57, 0.75, 0.86, 0.94, 0.99])
coverage['5ppm'] = ([0, 5, 10, 15, 20, 25, 30, 60], [0, 0.03, 0.15, 0.22, 0.33, 0.38, 0.48, 0.7])



fig = plt.figure()
ax = fig.add_subplot(111)
ax.tick_params(axis='both', which='major', labelsize=20)
plt.xlabel('t/min', fontsize=20)
ax.set_prop_cycle(cycler('color', ['c', 'b', 'r', 'k']))
ax.set_ylabel("Graphene Coverage (ML)", fontsize=20)
ax.plot(coverage['30ppm'][0], coverage['30ppm'][1], '--o', label='30ppm')
ax.plot(coverage['20ppm'][0], coverage['20ppm'][1], '--o', label='20ppm')
ax.plot(coverage['10ppm'][0], coverage['10ppm'][1], '--o', label='10ppm')
ax.plot(coverage['5ppm'][0], coverage['5ppm'][1], '--o', label='5ppm')

ax.legend(loc=0, numpoints=1, fontsize=15)
ax.grid(True)
plt.savefig('methane_effect.eps', format='eps', dpi=1000)
plt.savefig('/Users/raymon/Google Drive/UH/dissertation/dissertation/figure/chapter2/methane_effect.eps', format='eps', dpi=1000)
plt.show()