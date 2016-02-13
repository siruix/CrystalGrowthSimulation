from __future__ import division
from math import exp
from math import log
# Model
# k_plus = gamma * exp(beta * mu)               (1)
# k_plus = k_eq * exp(beta * delta_mu)          (2) from (1)
# k_minus = gamma * exp(-m * beta * phi)        (3)
# k_eq = gamma * exp(-1.5 * beta * phi)           (4) according to equilibrium
# put (4) into (2),
# k_plus = gamma * exp(-1.5 * beta * phi) * exp(beta * delta_mu)
# k_migration = gamma_migration * exp(-m * beta * phi * (phi_c/(phi_c+phi_cu))

Boltzmann = 1.38064852e-23
Electron_charge = 1.60217662e-19

class Config(object):
    # global variables
    RANDOM_SEED = 42
    SCOPE_SIZE = 50
    NUM_ATOM = SCOPE_SIZE * SCOPE_SIZE * 2 * 0.1
    SIM_TIME = None   # Simulation time in sim clock
    GAMMA = 0.5        # migration frequency factor
    # ratio is the migration rate to evaporation rate.
    # Girit, 2009.  says 2-3 order
    migration_ratio = 1e3
    # simulation real time limit in minutes
    time_limit = 60
    temperature = 1000

    # [Girit, 2009] one sigma 0.3eV - 0.6eV, two sigma 6eV, three sigma 9eV
    # I include delocalize effect, so sigma bond energy is weaker.
    # sigma bond
    eVs = [0, 0.2, 0.7, 3]
    # pi bond larger the stronger ring
    delocalized_eV = 0.1
    # phi_c / (phi_c + phi_cu)
    ratio_c = 1.0
    # target coverage
    C = 0.5
    # # weight of delocalize effect
    # weight_delocalize = 1.7
    delocalized_rate = []
    migration_rate_by_num_neighbor = []
    evaporation_rate_by_num_neighbor = []
    DEPOSITION_RATE = 0
    DEPOSITION_RATE_PER_SITE = 0


    @classmethod
    def setParameters(cls, delta_mu):

        gamma_mig = Config.GAMMA
        for eV in Config.eVs:
            Config.migration_rate_by_num_neighbor.append(gamma_mig * eV2Rate(eV*Config.ratio_c))

        gamma_eva = gamma_mig / Config.migration_ratio
        for eV in Config.eVs:
            Config.evaporation_rate_by_num_neighbor.append(gamma_eva*eV2Rate(eV))

        Config.delocalized_rate = [eV2Rate(i*Config.delocalized_eV) for i in range(13)]
        # use 2 bonds as zigzag prevail at equilibrium
        k_eq = gamma_eva * eV2Rate(Config.eVs[2]) / (1-Config.C)
        cls.DEPOSITION_RATE_PER_SITE = k_plus = k_eq * eV2Rate(-delta_mu)
        cls.DEPOSITION_RATE = cls.DEPOSITION_RATE_PER_SITE * cls.SCOPE_SIZE * cls.SCOPE_SIZE

    @classmethod
    def getAdAtomMigrationRate(cls):
        return Config.migration_rate_by_num_neighbor[0]

    @classmethod
    def getDimerMigrationRate(cls):
        return 4.0/9.0 * Config.migration_rate_by_num_neighbor[1]

    @classmethod
    def getTrimerMigrationRate(cls):
        return 5.0/27.0 * Config.migration_rate_by_num_neighbor[1]

def eV2Rate(eV):
    return exp(-eV*Electron_charge/Boltzmann/(Config.temperature+273))