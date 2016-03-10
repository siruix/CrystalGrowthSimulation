from __future__ import division
from  model import *
import matplotlib.pylab as plt
import numpy as np
from scipy.integrate import odeint
# plot config
use_log_scale = True

#####################################
# Experimental data Ref: Wu. Two-step growth
coverage = {}
coverage['30ppm'] = ([0, 5, 10, 15, 20], [0, 0.78, 0.97, 0.99, 1])
coverage['20ppm'] = ([0, 5, 10, 15, 20, 25, 30], [0, 0.58, 0.83, 0.94, 0.96, 0.99, 1])
coverage['10ppm'] = ([0, 5, 10, 15, 20, 25, 30, 60], [0, 0.19, 0.38, 0.57, 0.75, 0.86, 0.94, 0.99])
coverage['5ppm'] = ([0, 5, 10, 15, 20, 25, 30, 60], [0, 0.03, 0.15, 0.22, 0.33, 0.38, 0.48, 0.7])

c_ch4 = 30e-6
Config.setParameters(c_ch4)
####### nucleation zone ########
y0 = [0, 0, 0, 0, 0, 0]
sigma = 1e-8
para = (sigma, sigma, sigma, sigma, Config.decay_rate)
t = np.linspace(0, 1e-5, 10000)
sol = odeint(f_rate2, y0, t, args=(para,))
# plot results
fig0 = plt.figure()
ax0 = fig0.add_subplot(111)
ax01 = ax0.twinx()
ax01.set_ylabel("Coverage")
if use_log_scale is True:
    ax0.loglog(t, sol[:, 0], 'r-', label='#Active Carbon')
    ax0.loglog(t, sol[:, 1], 'b-', label='#Dimmer')
    # ax0.loglog(t, sol[:, 1], 'g-', label='#Unstable cluster')
    ax0.loglog(t, sol[:, 2], 'k-', label='#Stable cluster')
    ax0.loglog(t, sol[:, 3], 'c-', label='Stable cluster area')
    ax0.loglog(t, sol[:, 4], 'y-', label='Defect-induced cluster area')
    ax01.loglog(t, sol[:,5], 'mo', label='Coverage')
else:
    ax0.plot(t, sol[:, 0], 'r-', label='#Active Carbon')
    ax0.plot(t, sol[:, 1], 'b-', label='#Dimmer')
    # ax0.plot(t, sol[:, 1], 'g-', label='#Unstable cluster')
    ax0.plot(t, sol[:, 2], 'k-', label='#Stable cluster')
    ax0.plot(t, sol[:, 3], 'c-', label='Stable cluster area')
    ax0.plot(t, sol[:, 4], 'y-', label='Defect-induced cluster area')
# ax1.axhline(y=n0, xmin=0, xmax=t[-1])
ax0.set_ylabel("$Density\,cm^{2}$")
ax0.legend(loc=0)
plt.xlabel('t')
plt.title('nucleation zone')
# ax01 = ax0.twinx()
# l4 = ax01.loglog(t, sol[:, 6], 'm-', label='Coverage')
# ax01.set_ylabel("Coverage")
# ax01.legend(loc=2)

####### growth zone ########
t = np.linspace(0, 1e-1, 10000)
sol = odeint(f_rate2, y0, t, args=(para,))
# plot results
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax11 = ax1.twinx()
ax11.set_ylabel("Coverage")
if use_log_scale is True:
    ax1.loglog(t, sol[:, 0], 'r-', label='#Active Carbon')
    ax1.loglog(t, sol[:, 1], 'b-', label='#Dimmer')
    # ax1.loglog(t, sol[:, 2], 'g-', label='#Unstable cluster')
    ax1.loglog(t, sol[:, 2], 'k-', label='#Stable cluster')
    ax1.loglog(t, sol[:, 3], 'c-', label='Stable cluster area')
    ax1.loglog(t, sol[:, 4], 'y-', label='Defect-induced cluster area')
    ax11.loglog(t, sol[:,5], 'mo', label='Coverage')
else:
    ax1.plot(t, sol[:, 0], 'r-', label='#Active Carbon')
    # ax1.plot(t, sol[:, 1], 'b-', label='#Dimmer')
    ax1.plot(t, sol[:, 1], 'g-', label='#Unstable cluster')
    ax1.plot(t, sol[:, 2], 'k-', label='#Stable cluster')
    ax1.plot(t, sol[:, 3], 'c-', label='Stable cluster area')
    ax1.plot(t, sol[:, 4], 'y-', label='Defect-induced cluster area')
# ax1.axhline(y=n0, xmin=0, xmax=t[-1])
ax1.set_ylabel("$Density\,cm^{2}$")
ax1.legend(loc=0)
plt.xlabel('t')
plt.title('growth zone')
# ax2 = ax1.twinx()
# ax2.loglog(t, sol[:, 6], 'm-', label='Coverage')
# ax2.set_ylabel("Coverage")
# ax2.legend(loc=2)

####### High coverage zone ########
t = np.linspace(0, 60*60, 10000)
sol = odeint(f_rate2, y0, t, args=(para,), mxstep=100000)
# plot results
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.set_ylabel("$Density\,cm^{2}$")
plt.xlabel('t')
plt.title('High coverage zone')
ax21 = ax2.twinx()
ax21.set_ylabel("Coverage")

if use_log_scale is True:
    ax2.loglog(t, sol[:, 0], 'r-', label='#Active Carbon')
    ax2.loglog(t, sol[:, 1], 'b-', label='#Dimmer')
    # ax2.loglog(t, sol[:, 1], 'g-', label='#Unstable cluster')
    ax2.loglog(t, sol[:, 2], 'k-', label='#Stable cluster')
    ax2.loglog(t, sol[:, 3], 'c-', label='Stable cluster area')
    ax2.loglog(t, sol[:, 4], 'y-', label='Defect-induced cluster area')
    ax21.loglog(t, sol[:,5], 'mo', label='Coverage')
else:
    t_min = np.divide(t, 60)
    ax21.plot(coverage['5ppm'][0], coverage['5ppm'][1], 'ko', label='5ppm')
    ax21.plot(coverage['10ppm'][0], coverage['10ppm'][1], 'ro', label='10ppm')
    ax21.plot(coverage['20ppm'][0], coverage['20ppm'][1], 'bo', label='20ppm')
    ax21.plot(coverage['30ppm'][0], coverage['30ppm'][1], 'co', label='30ppm')
    ax21.plot(t_min, sol[:, 5], 'm-', label='Coverage')

ax2.legend(loc=0)
ax21.legend(loc=0)
ax2.grid(True)
#####################################
plt.show()
#
# fig2 = plt.figure()
# ax = fig2.add_subplot(111)
# # ax.plot(sol[:, 3], sol[:, 0], 'ro', label='CH4')
# ax.loglog(sol[:, 3], sol[:, 1]/n0, 'b-', label='n1')
# ax.loglog(sol[:, 3], sol[:, 2]/n0, 'g-', label='nx')
# ax.legend(loc=4)
# ax.set_ylabel("Island density ML")
# plt.xlabel('Coverage')
# plt.show()

