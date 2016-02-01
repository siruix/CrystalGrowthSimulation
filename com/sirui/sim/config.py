# config.py

RANDOM_SEED = 42
SCOPE_SIZE = 30
NUM_ATOM = 500
SIM_TIME = 1000     # Simulation time in sim clock

# per sim clock per site
# k_plus = k_eq * exp({delta_mu} / kT)
DEPOSITION_RATE_PER_SITE = 0.001

# per sim clock of sim field.
# TODO can be a fraction of atom per clock
DEPOSITION_RATE = DEPOSITION_RATE_PER_SITE * SCOPE_SIZE * SCOPE_SIZE

# k_m = v*exp(-m*{phi}/kT)
# depends on atom's #neighbor
# EVAPORATION_RATE_PER_SITE =




# runtime global variable
