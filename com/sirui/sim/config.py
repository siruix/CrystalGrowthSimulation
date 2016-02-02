# config.py
from math import exp
RANDOM_SEED = 42
SCOPE_SIZE = 30
NUM_ATOM = 100
SIM_TIME = 1000     # Simulation time in sim clock

# simulation parameters
beta_phi = 2.0
beta_delta_mu = 2.0

# k_plus = k_eq * exp(beta * delta_mu)
# k_minus = gamma * exp(-m * beta * phi)
# k_eq = gamma * exp(-2 * beta * phi)


# set evaporation rate a reasonable value
gamma_eva = evaporation_rate_0neighbor = 0.01
evaporation_rate_1neighbor = gamma_eva * exp(-beta_phi)
evaporation_rate_2neighbor = gamma_eva * exp(-2*beta_phi)
evaporation_rate_3neighbor = gamma_eva * exp(-3*beta_phi)
evaporation_rate_4neighbor = gamma_eva * exp(-4*beta_phi)
evaporation_period_0neighbor = round(1.0 / evaporation_rate_0neighbor)
evaporation_period_1neighbor = round(1.0 / evaporation_rate_1neighbor)
evaporation_period_2neighbor = round(1.0 / evaporation_rate_2neighbor)
evaporation_period_3neighbor = round(1.0 / evaporation_rate_3neighbor)
evaporation_period_4neighbor = round(1.0 / evaporation_rate_4neighbor)

# ratio is the migration rate to evaporation rate
ratio = 10.0
gamma_mig = migration_rate_0neighbor = ratio * gamma_eva
migration_rate_1neighbor = gamma_mig * exp(-beta_phi)
migration_rate_2neighbor = gamma_mig * exp(-2*beta_phi)
migration_rate_3neighbor = gamma_mig * exp(-3*beta_phi)
migration_rate_4neighbor = gamma_mig * exp(-4*beta_phi)
migration_period_0neighbor = round(1.0 / migration_rate_0neighbor)
migration_period_1neighbor = round(1.0 / migration_rate_1neighbor)
migration_period_2neighbor = round(1.0 / migration_rate_2neighbor)
migration_period_3neighbor = round(1.0 / migration_rate_3neighbor)
migration_period_4neighbor = round(1.0 / migration_rate_4neighbor)



# per sim clock per site
# k_plus = k_eq * exp(beta * delta_mu)
# deposition rate
k_eq = gamma_eva * exp(-2*beta_phi)
DEPOSITION_RATE_PER_SITE = k_plus = k_eq * exp(beta_delta_mu)
# DEPOSITION_RATE_PER_SITE = 0.001
# per sim clock of sim field.
DEPOSITION_RATE = DEPOSITION_RATE_PER_SITE * SCOPE_SIZE * SCOPE_SIZE
