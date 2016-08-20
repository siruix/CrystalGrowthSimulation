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

rate = {}
# rate['30ppm'] = ([0, 5, 10, 15, 20], [0.78, 0.19, 0.02, 0.01, 0])
# rate['20ppm'] = ([0, 5, 10, 15, 20, 25, 30], [0.58, 0.25, 0.11, 0.02, 0.03, 0.01, 0])
# rate['10ppm'] = ([0, 5, 10, 15, 20, 25, 30, 60], [0.19, 0.19, 0.19, 0.18, 0.11, 0.08, 0.05, 0])
# rate['5ppm'] = ([0, 5, 10, 15, 20, 25, 30], [0.03, 0.12, 0.07, 0.11, 0.05, 0.1, 0.1])
rate['30ppm'] = ([0.78, 0.97, 0.99], [0.097, 0.021, 0.003])
rate['20ppm'] = ([0.58, 0.83, 0.94, 0.96, 0.99], [0.083, 0.036, 0.013, 0.005, 0.004])
rate['10ppm'] = ([0.19, 0.38, 0.57, 0.75, 0.86, 0.94], [0.038, 0.038, 0.037, 0.029, 0.01, 0.0037])
rate['5ppm'] = ([0.03, 0.15, 0.22, 0.33, 0.38], [0.015, 0.019, 0.018, 0.016, 0.015])

fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.tick_params(axis='both', which='major', labelsize=15)
plt.xlabel('time ($min$)', fontsize=20)
ax.set_prop_cycle(cycler('color', ['c', 'b', 'r', 'k']))
ax.set_ylabel("Graphene Coverage (ML)", fontsize=20)
ax.plot(coverage['30ppm'][0], coverage['30ppm'][1], '--o', label='30 ppm')
ax.plot(coverage['20ppm'][0], coverage['20ppm'][1], '--o', label='20 ppm')
ax.plot(coverage['10ppm'][0], coverage['10ppm'][1], '--o', label='10 ppm')
ax.plot(coverage['5ppm'][0], coverage['5ppm'][1], '--o', label='  5 ppm')

ax.legend(loc=0, numpoints=1, fontsize=15)
ax.grid(True)
plt.savefig('methane_effect.eps', format='eps', dpi=1000)
plt.savefig('/Users/raymon/Google Drive/UH/dissertation/dissertation/figure/chapter3/methane_effect.eps', format='eps', dpi=1000)


########## growth rate ########
fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
ax2.tick_params(axis='both', which='major', labelsize=15)
plt.xlabel('Coverage (ML)', fontsize=20)
ax2.set_prop_cycle(cycler('color', ['c', 'b', 'r', 'k']))
ax2.set_ylabel("Graphene Growth Rate (ML/min)", fontsize=20)
ax2.plot(rate['30ppm'][0], rate['30ppm'][1], '--o', label='30 ppm')
ax2.plot(rate['20ppm'][0], rate['20ppm'][1], '--o', label='20 ppm')
ax2.plot(rate['10ppm'][0], rate['10ppm'][1], '--o', label='10 ppm')
ax2.plot(rate['5ppm'][0], rate['5ppm'][1], '--o', label='  5 ppm')

ax2.legend(loc=0, numpoints=1, fontsize=15)
ax2.grid(True)
plt.savefig('methane_effect_rate.eps', format='eps', dpi=1000)
plt.savefig('/Users/raymon/Google Drive/UH/dissertation/dissertation/figure/chapter3/methane_effect_rate.eps', format='eps', dpi=1000)



plt.show()