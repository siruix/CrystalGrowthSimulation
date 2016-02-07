# config.py
from math import exp
# Model
# k_plus = gamma * exp(beta * mu)               (1)
# k_plus = k_eq * exp(beta * delta_mu)          (2) from (1)
# k_minus = gamma * exp(-m * beta * phi)        (3)
# k_eq = gamma * exp(-1.5 * beta * phi)           (4) according to equilibrium
# put (4) into (2),
# k_plus = gamma * exp(-1.5 * beta * phi) * exp(beta * delta_mu)
# k_migration = gamma_migration * exp(-m * beta * phi)

class Config(object):
    # global variables
    # RANDOM_SEED = 42
    SCOPE_SIZE = 30
    NUM_ATOM = SCOPE_SIZE * SCOPE_SIZE * 2 * 0
    SIM_TIME = 1000    # Simulation time in sim clock
    GAMMA = 0.01        # frequency factor
    # ratio is the migration rate to evaporation rate
    ratio = 1e2

    migration_rate_by_num_neighbor = []
    evaporation_rate_by_num_neighbor = []
    DEPOSITION_RATE = 0
    DEPOSITION_RATE_PER_SITE = 0

    @classmethod
    def setParameters(cls, beta_phi, beta_delta_mu):


        # set evaporation rate a reasonable value
        gamma_eva = Config.GAMMA
        Config.evaporation_rate_by_num_neighbor.append(gamma_eva)
        Config.evaporation_rate_by_num_neighbor.append(gamma_eva * exp(-beta_phi))
        Config.evaporation_rate_by_num_neighbor.append(gamma_eva * exp(-2*beta_phi))
        Config.evaporation_rate_by_num_neighbor.append(gamma_eva * exp(-3*beta_phi))

        gamma_mig = Config.ratio * gamma_eva
        Config.migration_rate_by_num_neighbor.append(gamma_mig)
        Config.migration_rate_by_num_neighbor.append(gamma_mig * exp(-beta_phi))
        Config.migration_rate_by_num_neighbor.append(gamma_mig * exp(-2*beta_phi))
        Config.migration_rate_by_num_neighbor.append(gamma_mig * exp(-3*beta_phi))



        # per sim clock per site
        # k_plus = k_eq * exp(beta * delta_mu)
        # deposition rate
        k_eq = gamma_eva * exp(-1.5*beta_phi)
        cls.DEPOSITION_RATE_PER_SITE = k_plus = k_eq * exp(beta_delta_mu)
        # DEPOSITION_RATE_PER_SITE = 0.001
        # per sim clock of sim field.
        cls.DEPOSITION_RATE = cls.DEPOSITION_RATE_PER_SITE * cls.SCOPE_SIZE * cls.SCOPE_SIZE

