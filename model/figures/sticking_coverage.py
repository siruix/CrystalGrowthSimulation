# to plot the precursor mediated adsorption sticking coefficient vs y
from __future__ import division
import matplotlib.pylab as plt
import numpy as np
from cycler import cycler

thetas = np.linspace(0, 1, 80, endpoint=False)
Kps = [1.0, 0.7, 0.4, 0.1, 0.01]

s = lambda theta,Kp: 1.0 / (1 + Kp*theta/(1-theta))
y = np.zeros((len(Kps),thetas.size))
for i,Kp in enumerate(Kps):
    for j,theta in enumerate(thetas):
        y[i][j] = s(theta, Kp)
        
fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.tick_params(axis='both', which='major', labelsize=15)
plt.xlabel('Coverage (ML)', fontsize=20)
# ax.set_prop_cycle(cycler('color', ['c', 'b', 'r', 'k', 'm']))
ax.set_ylabel("$s/s_0$", fontsize=20)
for i in range(len(Kps)):
    ax.plot(thetas, y[i], '-', label='Kp=%s'%Kps[i])

ax.legend(loc=0, numpoints=1, fontsize=15)
ax.grid(True)
plt.savefig('sticking.eps', format='eps', dpi=1000)
plt.savefig('/Users/raymon/Google Drive/UH/dissertation/dissertation/figure/chapter6/sticking.eps', format='eps', dpi=1000)



plt.show()