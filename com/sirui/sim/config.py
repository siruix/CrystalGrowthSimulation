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

k = 1.38064852e-23
e = 1.60217662e-19

class Config(object):
    # global variables
    RANDOM_SEED = 42
    SCOPE_SIZE = 50
    NUM_ATOM = SCOPE_SIZE * SCOPE_SIZE * 2 * 0.0
    SIM_TIME = None   # Simulation time in sim clock
    GAMMA = 0.5        # migration frequency factor
    # ratio is the migration rate to evaporation rate.
    # Girit, 2009.  says 2-3 order
    migration_ratio = 1e3
    # simulation real time limit in minutes
    time_limit = 20



    # phi_c / (phi_c + phi_cu)
    ratio_c = 1.0
    # target coverage
    # C = 0.5
    # # weight of delocalize effect
    # weight_delocalize = 1.7
    delocalized_rate = []
    migration_rate_by_num_neighbor = []
    evaporation_rate_by_num_neighbor = []
    DEPOSITION_RATE = 0
    DEPOSITION_RATE_PER_SITE = 0

    NUM_DEFECT = 3
    DEFECT_POSITIONS = []
    # temperature in C
    T = 1000
    # Active carbon species activation energy. The larger, the more temperature dependence
    Ea = 2.0
    # reference hydrocarbon amount (value not reflect physical)
    n0 = None
    # [Girit, 2009] one sigma 0.3eV - 0.6eV, two sigma 6eV, three sigma 9eV
    # I include delocalize effect, so sigma bond energy is weaker.
    # sigma bond
    sigma_bonds = [0, 0.1, 0.6, 3]
    # pi bond larger the stronger ring
    delocalized_eV = 1e-2


    @classmethod
    def setParameters(cls, kn):

        gamma_mig = Config.GAMMA
        for phi in Config.sigma_bonds:
            Config.migration_rate_by_num_neighbor.append(gamma_mig * eV2Rate(phi * Config.ratio_c))

        gamma_eva = gamma_mig / Config.migration_ratio
        for phi in Config.sigma_bonds:
            Config.evaporation_rate_by_num_neighbor.append(gamma_eva * eV2Rate(phi))

        Config.delocalized_rate = [eV2Rate(i*Config.delocalized_eV) for i in range(13)]

        Config.n0 = log(0.1)*exp(e*Config.Ea/k/(Config.T+273))
        # Does not use equilibrium condition
        cls.DEPOSITION_RATE_PER_SITE = k_plus = gamma_eva*exp(kn*Config.n0*eV2Rate(Config.Ea))
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
    return exp(-eV * e / k / (Config.T + 273))

