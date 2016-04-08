import matplotlib.pylab as plt
from cycler import cycler

#####################################
# Experimental data Ref: Xing. Kinetic.
time = [0, 5, 10, 15, 20, 30, 60]
coverage = {}
coverage['1050'] = (time, [0, 0.5718, 0.824, 0.9665, 0.9862, 1, 1])
coverage['1025'] = (time, [0, 0.4875, 0.6845, 0.8752, 0.9342, 0.9912, 1])
coverage['1000'] = (time, [0, 0.2, 0.5307, 0.6911, 0.817, 0.8735, 0.9897])
coverage['950'] =  (time, [0, 0.1085, 0.2629, 0.4527, 0.5409, 0.6104, 0.8266])
coverage['900'] =  (time, [0, 0.072, 0.1208, 0.131, 0.1382, 0.1942, 0.3542])

rate = {}
rate['1050'] = ([0.5718, 0.824, 0.9665, 0.9862], [0.0824, 0.0395, 0.0162, 0.0022])
rate['1025'] = ([0.4875, 0.6845, 0.8752, 0.9342], [0.0685, 0.0388, 0.025, 0.0077])
rate['1000'] = ([0.2, 0.5307, 0.6911, 0.817], [0.0531, 0.0491, 0.0286, 0.0122])
rate['950'] =  ([0.1085, 0.2629, 0.4527, 0.5409], [0.0263, 0.0344, 0.0278, 0.0105])
rate['900'] =  ([0.072, 0.1208, 0.131, 0.1382], [0.0121, 0.014, 0.0017, 0.0042])


fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.set_prop_cycle(cycler('color', ['c', 'b', 'r', 'k', 'm']))
ax.tick_params(axis='both', which='major', labelsize=20)
plt.xlabel('t (min)', fontsize=20)
ax.set_ylabel("Graphene Coverage (ML)", fontsize=20)
ax.plot(coverage['1050'][0], coverage['1050'][1], '--o', label='1050$^\circ$C')
ax.plot(coverage['1025'][0], coverage['1025'][1], '--o', label='1025$^\circ$C')
ax.plot(coverage['1000'][0], coverage['1000'][1], '--o', label='1000$^\circ$C')
ax.plot(coverage['950'][0], coverage['950'][1], '--o', label=' 950$^\circ$C')
ax.plot(coverage['900'][0], coverage['900'][1], '--o', label=' 900$^\circ$C')


ax.legend(loc=0, numpoints=1, fontsize=15)
ax.grid(True)
#####################################
plt.savefig('temperature_effect.eps', format='eps', dpi=1000)
plt.savefig('/Users/raymon/Google Drive/UH/dissertation/dissertation/figure/chapter3/temperature_effect.eps', format='eps', dpi=1000)




########## growth rate ########
fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
ax2.tick_params(axis='both', which='major', labelsize=20)
ax2.set_prop_cycle(cycler('color', ['c', 'b', 'r', 'k', 'm']))
plt.xlabel('Coverage (ML)', fontsize=20)
ax2.set_ylabel("Graphene Growth Rate (ML / min)", fontsize=20)
ax2.plot(rate['1050'][0], rate['1050'][1], '--o', label='1050$^\circ$C')
ax2.plot(rate['1025'][0], rate['1025'][1], '--o', label='1025$^\circ$C')
ax2.plot(rate['1000'][0], rate['1000'][1], '--o', label='1000$^\circ$C')
ax2.plot(rate['950'][0], rate['950'][1], '--o', label='950$^\circ$C')
ax2.plot(rate['900'][0], rate['900'][1], '--o', label='900$^\circ$C')

ax2.legend(loc=0, numpoints=1, fontsize=15)
ax2.grid(True)
plt.savefig('temperature_effect_rate.eps', format='eps', dpi=1000)
plt.savefig('/Users/raymon/Google Drive/UH/dissertation/dissertation/figure/chapter3/temperature_effect_rate.eps', format='eps', dpi=1000)




plt.show()
