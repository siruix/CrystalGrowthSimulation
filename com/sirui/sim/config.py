from __future__ import division
import math
# Model
# Solid on Solid model. Each atom can only occupy one site. Every site identical.
# Adsorption
# k_plus = gamma * exp(beta * mu)               (1)
# k_plus = k_eq * exp(beta * delta_mu)          (2) from (1)
# Desorption
# k_minus = gamma * exp(-m * beta * phi)        (3)
# k_eq = gamma * exp(-2 * beta * phi)           (4) according to equilibrium
# put (4) into (2),
# k_plus = gamma * exp(-2 * beta * phi) * exp(beta * delta_mu)
# Diffusion
# k_diff = gamma_diff * exp(-m*beta*phi)

# k = 1.38064852e-23
# e = 1.60217662e-19

class Config(object):
    # global variables
    RANDOM_SEED = 42
    SCOPE_SIZE = 50
    SCOPE_HEIGHT = 20
    NUM_ATOM = SCOPE_SIZE * SCOPE_SIZE * 2 * 0.0  # initial atom
    SIM_TIME = None   # Simulation time in sim clock. None means unlimited
    GAMMA = 0.5        # lattice vibration frequency factor. Use as migration rate.

    # simulation real time limit in minutes. Set upper bound for simulation time.
    time_limit = 20

    desorption_rate_by_num_neighbor = []
    diffusion_rate_by_num_neighbor = []
    ADSORPTION_RATE = 0
    ADSORPTION_RATE_PER_SITE = 0

    @classmethod
    def setParameters(cls, delta_mu, phi):
        Config.delta_mu = delta_mu
        Config.phi = phi
        gamma_des = Config.GAMMA/10
        for i in range(6):
            Config.desorption_rate_by_num_neighbor.append(gamma_des * math.exp(-i * Config.phi))
        # set diffusion rate 10 time larger than desorption rate
        for i in range(6):
            Config.diffusion_rate_by_num_neighbor.append(Config.GAMMA * math.exp(-i * Config.phi))

        # equilibrium condition
        k_eq = gamma_des*math.exp(-2*Config.phi)

        cls.ADSORPTION_RATE_PER_SITE = k_eq * math.exp(Config.delta_mu)
        cls.ADSORPTION_RATE = cls.ADSORPTION_RATE_PER_SITE * cls.SCOPE_SIZE * cls.SCOPE_SIZE
