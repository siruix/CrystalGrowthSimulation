from __future__ import division
import math
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config(object):
    """
    unit area is cm^2
    unit time is second
    """
    # define experiment parameters
    # CH4 concentration
    c_ch4 = None

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
    p = None
    # CH4 mass per molecular in kg
    m = 16.04e-3 / Na
    # impingement. molecular per second per square-centimeter
    I = None
    # phase change coeff
    K = 1
    #############################################
    # Adsorption
    # Assume first-order non-dissociative non-activate adsorption

    # condensation coefficient. Prob gas trapped in precursor state.
    alpha = 1

    E_d = 0.01
    E_a = 1.59
    # initial sticking coeff
    s0 = None
    #############################################
    # Desorption of CH3
    # Assume first-order. No adsorbed atom interaction.
    # atomic frequency of crystal lattice
    gamma_des0 = 1e13
    # energy barrier to desorb in eV. Larger, the more CH4 accumulation
    E_des = 1.4#0.7
    # life time of adsorbate on surface
    k_des = None
    #############################################
    # Diffusion
    # energy barrier to diffuse for CHx in eV
    E_diff = 0.1 # a guess. typically 5-20% of E_des
    # Diffusion pre-factor. Larger the longer diffusion
    # oscillation frequency of atom. Attempt frequency to overcome barrier.
    gamma_diff = 1e13 #
    # adsorption site spacing in centimeter
    a = 3.615e-8 #? lattice space
    # adsorption site per cm^2
    n0 = 1 / math.pow(a, 2)
    # Diffusion of CHx in cm^2 per second
    D = None

    ############################################
    # Defect
    # defect site per cm^2
    nd = None
    ############################################
    # CH3(a) to CHx activation energy barrier in eV
    E_act = 1.55 # ref: First-principle 1.55 to 1.61
    # coefficient. Larger the more CHx
    A_const = 1e13 # let's fix this
    # reaction rate CH4 to CHx
    k_act = None

    # CHx to CH3(a) activation energy barrier in eV
    E_deact = 0.71 # ref: First-principle
    # coefficient. Smaller the more CHx, the more nucleation
    B_const = 1e12 # tun larger to delay the start time
    # reaction rate CHx to CH4
    k_deact = None
    ############################################
    # decay rate coefficient. Attempt frequency decay.
    gamma_decay = 1e13
    delta_E_decay = 3.5 #larger the slower decay. More nucleation. Start time same. A reasonable guess.
    decay_rate = None
    ############################################
    # capture coefficient
    sigma = 1
    sigma_s = 0.2

    @classmethod
    def setParameters(cls, c_ch4, T = 1050+273, nd=0):
        logger.info('######################## Useful Intermediate Parameters ########################')
        Config.c_ch4 = c_ch4 * 2 # 2 time bias compensation.
        logger.info('c_ch4:%e'%Config.c_ch4)
        Config.p = Config.c_ch4 * Config.p0
        logger.info('p:%e'%Config.p)
        Config.I = Config.p / math.sqrt(2*math.pi*Config.m*Config.k_B*T) * 1e-4
        logger.info('I:%e'%Config.I)
        Config.s0 = Config.alpha / (1 + math.exp(-Config.e*(Config.E_d - Config.E_a)/Config.k_B/T))
        logger.info('s0:%e'%Config.s0)
        Config.k_des = Config.gamma_des0 * math.exp(-Config.e * Config.E_des / Config.k_B / T)
        logger.info('k_des: %e' % Config.k_des)
        Config.D = Config.gamma_diff/4/Config.n0 * math.exp(-Config.e*Config.E_diff/Config.k_B/T)
        logger.info('Diffusion coefficient:%e'%Config.D)
        Config.k_act = Config.A_const * math.exp(-Config.e * Config.E_act / Config.k_B / T)
        logger.info('k_act:%e' % Config.k_act)
        Config.k_deact = Config.B_const * math.exp(-Config.e * Config.E_deact / Config.k_B / T)
        logger.info('k_deact:%e' % Config.k_deact)
        Config.decay_rate = Config.gamma_decay*math.exp(-Config.e*Config.delta_E_decay/Config.k_B/T)
        logger.info('decay:%e'%Config.decay_rate)
        Config.nd = nd
        logger.info('nd:%e'%Config.nd)

    @staticmethod
    def s(theta, Kp=1):
        # precursor mediated
        # assume B = 0. Precursor complete disorder. theta00 = 1 - theta
        # Kp = 1 fall back to Langmuir.
        return Config.s0/(1+Kp*theta/(1-theta))