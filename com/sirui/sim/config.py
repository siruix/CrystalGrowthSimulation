# config.py
from math import exp



class Config(object):
    # global variables
    RANDOM_SEED = 42
    SCOPE_SIZE = 30
    NUM_ATOM = 100
    SIM_TIME = 1000     # Simulation time in sim clock
    migration_period_0neighbor = 0
    migration_period_1neighbor = 0
    migration_period_2neighbor = 0
    migration_period_3neighbor = 0
    migration_period_4neighbor = 0
    evaporation_period_0neighbor = 0
    evaporation_period_1neighbor = 0
    evaporation_period_2neighbor = 0
    evaporation_period_3neighbor = 0
    evaporation_period_4neighbor = 0
    DEPOSITION_RATE = 0

    @classmethod
    def setParameters(cls, beta_phi, beta_delta_mu):
        # k_plus = k_eq * exp(beta * delta_mu)
        # k_minus = gamma * exp(-m * beta * phi)
        # k_eq = gamma * exp(-2 * beta * phi)

        # set evaporation rate a reasonable value
        gamma_eva = evaporation_rate_0neighbor = 0.01
        evaporation_rate_1neighbor = gamma_eva * exp(-beta_phi)
        evaporation_rate_2neighbor = gamma_eva * exp(-2*beta_phi)
        evaporation_rate_3neighbor = gamma_eva * exp(-3*beta_phi)
        evaporation_rate_4neighbor = gamma_eva * exp(-4*beta_phi)
        cls.evaporation_period_0neighbor = round(1.0 / evaporation_rate_0neighbor)
        cls.evaporation_period_1neighbor = round(1.0 / evaporation_rate_1neighbor)
        cls.evaporation_period_2neighbor = round(1.0 / evaporation_rate_2neighbor)
        cls.evaporation_period_3neighbor = round(1.0 / evaporation_rate_3neighbor)
        cls.evaporation_period_4neighbor = round(1.0 / evaporation_rate_4neighbor)

        # ratio is the migration rate to evaporation rate
        ratio = 10.0
        gamma_mig = migration_rate_0neighbor = ratio * gamma_eva
        migration_rate_1neighbor = gamma_mig * exp(-beta_phi)
        migration_rate_2neighbor = gamma_mig * exp(-2*beta_phi)
        migration_rate_3neighbor = gamma_mig * exp(-3*beta_phi)
        migration_rate_4neighbor = gamma_mig * exp(-4*beta_phi)
        cls.migration_period_0neighbor = round(1.0 / migration_rate_0neighbor)
        cls.migration_period_1neighbor = round(1.0 / migration_rate_1neighbor)
        cls.migration_period_2neighbor = round(1.0 / migration_rate_2neighbor)
        cls.migration_period_3neighbor = round(1.0 / migration_rate_3neighbor)
        cls.migration_period_4neighbor = round(1.0 / migration_rate_4neighbor)



        # per sim clock per site
        # k_plus = k_eq * exp(beta * delta_mu)
        # deposition rate
        k_eq = gamma_eva * exp(-2*beta_phi)
        DEPOSITION_RATE_PER_SITE = k_plus = k_eq * exp(beta_delta_mu)
        # DEPOSITION_RATE_PER_SITE = 0.001
        # per sim clock of sim field.
        cls.DEPOSITION_RATE = DEPOSITION_RATE_PER_SITE * cls.SCOPE_SIZE * cls.SCOPE_SIZE

