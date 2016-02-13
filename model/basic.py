import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from math import exp

def f(y, t, params):
    C = y      # unpack current values of y
    beta_phi, gamma, gamma_mu, k, T, Ea_c = params  # unpack parameters
    derivs = gamma*exp((gamma_mu*exp(-e*Ea_c/k/T))/k/T)*(1-C) - gamma*exp(-3*C*beta_phi)*C
    return derivs

# Parameters
gamma = 1e-2               # frequency factor
gamma_mu = 0                # mu temperature dependance
Ea_c = 1                    # CH4 -> CHx 1 to 2. 
e = 1.60217662e-19          # electron charge
k = 1.38064852e-23          # Bolzmann constant
Ts = [1050, 1030, 1010, 980, 950]              # temperature
# T = 1000
beta_phi = 1.0                   # sigma bond 

# beta_delta_mus = [0.0, 1.0, 2.0, 3.0, 4.0]              # driving potential

# Initial values
C0 = 0.0     # initial coverage
# Ce = 0.95     # equilibrium coverage
coverage = {}
tStop = 100.
tInc = 0.1
# Make time array for solution
t = np.arange(0., tStop, tInc)
# Bundle initial conditions for ODE solver
y0 = [C0]
for T in Ts:
    # Bundle parameters for ODE solver
    params = [beta_phi, gamma, gamma_mu, k, T, Ea_c]
    # Call the ODE solver
    coverage[T] = odeint(f, y0, t, args=(params,))

# Plot results
fig = plt.figure(1, figsize=(8,8))
ax = fig.add_subplot(111)
# ax.plot(t, coverage[0.0][:], 'r-')
# ax.plot(t, coverage[1.0][:], 'm-')
# ax.plot(t, coverage[2.0][:], 'y-')
# ax.plot(t, coverage[3.0][:], 'g-')
# ax.plot(t, coverage[4.0][:], 'b-')
ax.plot(t, coverage[1050][:], 'r-')
ax.plot(t, coverage[1030][:], 'm-')
ax.plot(t, coverage[1010][:], 'y-')
ax.plot(t, coverage[980][:], 'g-')
ax.plot(t, coverage[950][:], 'b-')

plt.tight_layout()
plt.show()