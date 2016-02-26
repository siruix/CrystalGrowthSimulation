from __future__ import division
import matplotlib.pylab as plt
import numpy as np
import math
from scipy.integrate import odeint
from math import exp

# define experiment parameters
# CH4 flow in sccm
f_ch4 = 20
# Total flow in sccm
f = 1500
# Environment temperature in K
T = 1000 + 273

# Define constants
# ambient pressure in Pa
p0 = 101325
# Avogadro constant
Na = 6.022e23
# Boltzmann constant
k_B = 1.381e-23
# electron charge
e = 1.6e-19
# variables
# gas partial (in Pa)
p = f_ch4/f * p0
# CH4 mass per molecular in kg
m = 16.04e-3 / Na
# impingement. molecular per second per square-centimeter, then change to square-meter
I = p / math.sqrt(2*math.pi*m*k_B*T) * 1e4
print(I)
#############################################
# Adsorption
# Assume first-order non-dissociative non-activate adsorption
sigma_ads = 1
# sticking coefficient as function of surface site coverage. range varies a lot!!
s = lambda theta: sigma_ads * (1-theta)
# # num atom adsorb per unit time per unit area as function of surface site coverage
# r_ads = lambda theta: s(theta) * I
#############################################
# Desorption
# Assume first-order. No adsorbed atom interaction.
# atomic frequency of crystal lattice
gamma_des = 1e13
# larger the long life time in second
tau_CH4_0 = 1/gamma_des
# energy barrier to desorb in eV
E_des = 0.2#0.7
# life time of adsorbate on surface
tau_CH4 = tau_CH4_0 * math.exp(e*E_des/k_B/T)
#############################################
# Diffusion
# energy barrier to diffuse for CHx in eV
E_diff = 0.1 # a guess. typically 5-20% of E_d
# Diffusion pre-factor. Larger the longer diffusion
# oscillation frequency of atom. Attempt frequency to overcome barrier.
gamma_diff = 1e13 #?
# adsorption site spacing in meter
a = 3.615e-10#?
# adsorption site per square meter
n0 = 1 / math.pow(a, 2)
# defect site per square meter
nd = n0 * 0.0
# Diffusion of CHx in square meter per second
D = gamma_diff/4/n0 * math.exp(-e * E_diff / k_B / T)

############################################
# CH4 to CHx activation energy barrier in eV
E_a = 0.1#2.51
# coefficient. Larger the more CHx
A_const = 1#?
# reaction rate CH4 to CHx
k_a = A_const * math.exp(-e*E_a/k_B/T)
# CHx to CH4 activation energy barrier in eV
E_d = 10#0.65
# coefficient. Larger the less CHx
B_const = 0.1#?
# reaction rate CHx to CH4
k_d = B_const * math.exp(-e*E_d/k_B/T)
############################################
# decay rate coefficient. Attempt frequency decay.
gamma_decay = 1e13
# energy difference between 2-cluster and 1-cluster (eV). Larger the faster decay.
delta_E21 = 0.1 #?
# decay rate from 2-cluster to 1-cluster
delta_2 = gamma_decay * math.exp(-e*delta_E21/k_B/T)

###############################################
# rate equations. i = 1
# i - cluster : critical cluster size
# assume dimmer is stable. i = 1 (easiest case)
# n1 adatom density. Num of adatom per unit area. Time dependence.
#
def f_rate1(y, t, para):
    n_CH4, n1, nx, theta = y
    sigma1, sigmax = para
    # theta = (n_CH4 + n1 + nx)/n0
    dn_CH4_dt = s(theta) * I - n_CH4/tau_CH4 - k_a*n_CH4 + k_d*n1
    dn1_dt = k_a*n_CH4 - k_d*n1 - 2*sigma1*D*math.pow(n1,2) - n1*sigmax*D*nx
    dnx_dt = math.pow(n1,2)*sigma1*D
    dtheta_dt = (s(theta) * I - n_CH4/tau_CH4)/n0
    return [dn_CH4_dt, dn1_dt, dnx_dt, dtheta_dt]

###############################################
# rate equations i = 2
# i - cluster : critical cluster size
# assume dimmer is stable. i = 1 (easiest case)
# n1 adatom density. Num of adatom per unit area. Time dependence.
#
def f_rate2(y, t, para):
    # n - density (#cluster/m^2)
    # ax - total sites covered by stable cluster (#site/m^2)
    # ad - sites covered for each defect induced cluster (#site/cluster)
    n_CH4, n1, n2, nx, ax, ad, theta = y
    sigma_1,sigma_2,sigma_x,sigma_d,delta_2 = para
    dn_CH4_dt = s(theta) * I - n_CH4/tau_CH4 - k_a*n_CH4 + k_d*n1
    dn1_dt = k_a*n_CH4 - k_d*n1 - 2*sigma_1*D*math.pow(n1, 2) - sigma_2*D*n1*n2 +\
             2*delta_2*n2 - n1*sigma_x*D*ax - n1*sigma_d*D*ad*nd
    dn2_dt = sigma_1*D*math.pow(n1,2) - sigma_2*D*n1*n2 - delta_2*n2
    dnx_dt = sigma_2*D*n1*n2
    dax_dt = sigma_2*D*n1*n2 + sigma_x*D*n1*ax
    dad_dt = sigma_d*D*n1*nd
    dtheta_dt = (s(theta) * I - n_CH4/tau_CH4)/n0   # will lose count of some atom. Larger than real.
    return [dn_CH4_dt, dn1_dt, dn2_dt, dnx_dt, dax_dt, dad_dt, dtheta_dt]

####### nucleation zone ########
y0 = [0, 0, 0, 0, 0, 1, 0]
para = (1, 1, 1, 1, delta_2)
t = np.linspace(0, 1e-9, 100000)
sol = odeint(f_rate2, y0, t, args=(para,))
# plot results
fig0 = plt.figure()
ax0 = fig0.add_subplot(111)

l1 = ax0.loglog(t, sol[:, 0], 'r-', label='CH4 density')
l2 = ax0.loglog(t, sol[:, 1], 'b-', label='n1 density')
l3 = ax0.loglog(t, sol[:, 2], 'g-', label='nx density')
# ax1.axhline(y=n0, xmin=0, xmax=t[-1])
ax0.set_ylabel("$Density\,m^{2}$")
ax0.legend(loc=0)
plt.xlabel('t')
plt.title('nucleation zone')
ax02 = ax0.twinx()
l4 = ax02.loglog(t, sol[:, 3], 'm-', label='Coverage')
ax02.set_ylabel("Coverage")
ax02.legend(loc=2)

####### growth zone ########
y0 = [0, 0, 0, 0]
para = (1, 1)
t = np.linspace(0, 8.5e-1, 100000)
sol = odeint(f_rate, y0, t, args=(para,))
# plot results
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)

l1 = ax1.loglog(t, sol[:, 0], 'r-', label='CH4 density')
l2 = ax1.loglog(t, sol[:, 1], 'b-', label='n1 density')
l3 = ax1.loglog(t, sol[:, 2], 'g-', label='nx density')
# ax1.axhline(y=n0, xmin=0, xmax=t[-1])
ax1.set_ylabel("$Density\,m^{2}$")
ax1.legend(loc=0)
plt.xlabel('t')
plt.title('growth zone')
ax2 = ax1.twinx()
l4 = ax2.loglog(t, sol[:, 3], 'm-', label='Coverage')
# ax2.yaxis.tick_right()
# ax2.yaxis.set_label_position("right")
ax2.set_ylabel("Coverage")
# plt.legend((l1, l2, l3, l4), ("CH4", "CHx", "Stable", "Coverage"))
ax2.legend(loc=2)

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

