from __future__ import division
import math

class Config(object):

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

    #############################################
    # Adsorption
    # Assume first-order non-dissociative non-activate adsorption
    # sigma_ads = 1
    # condensation coefficient. Prob gas trapped in precursor state.
    # alpha = 1
    # rate constants
    # gamma_d = 1
    # gamma_a = 1
    # energy difference for precursor to [chemsorb - desorb]. Extracted from [Xing. Kinetic]
    # e_diff = 2.74 # positive for activated adsorption. Larger, the larger temperature dependence.
    # s0 = alpha / (1 + gamma_d/gamma_a*math.exp(e*e_diff)/k_B/T)
    s0 = 0.5
    print('s0:%e'%s0)
    # # num atom adsorb per unit time per unit area as function of surface site coverage
    # r_ads = lambda theta: s(theta) * I
    #############################################
    # Desorption
    # Assume first-order. No adsorbed atom interaction.
    # atomic frequency of crystal lattice
    gamma_des0 = 1e13
    # larger the long life time in second
    # tau_CH4_0 = 1/gamma_des
    # energy barrier to desorb in eV. Larger, the more CH4 accumulation
    E_des = 1.6#0.7
    # life time of adsorbate on surface
    k_des = None
    #############################################
    # Diffusion
    # energy barrier to diffuse for CHx in eV
    E_diff = 0.1 # a guess. typically 5-20% of E_des
    # Diffusion pre-factor. Larger the longer diffusion
    # oscillation frequency of atom. Attempt frequency to overcome barrier.
    gamma_diff = 1e13 #?
    # adsorption site spacing in centimeter
    a = 3.615e-8 #? lattice space
    # adsorption site per unit area
    n0 = 1 / math.pow(a, 2)
    print('n0:%e'%n0)
    # Diffusion of CHx in unit area per second
    D = None

    ############################################
    # Defect
    # defect site per unit area
    nd = n0 * 0 #1e-13
    ############################################
    # CH4(a) to CHx activation energy barrier in eV
    E_a = 2.5 #2.51 # ref: First-principle
    # coefficient. Larger the more CHx
    A_const = 5e10
    # reaction rate CH4 to CHx
    k_act = None

    # CHx to CH4(a) activation energy barrier in eV
    E_d = 0.65 # ref: First-principle
    # coefficient. Smaller the more CHx, the more nucleation
    B_const = 1e-2#?
    # reaction rate CHx to CH4
    k_deact = None
    # k_deact = 0 # assume no backward
    ############################################
    # decay rate coefficient. Attempt frequency decay.
    gamma_decay = 1e13
    # energy difference between 2-cluster and 1-cluster (eV). Larger the faster decay.
    delta_E_decay = 0.95 #larger the slower decay. More nucleation. Start time same.
    # decay rate from 2-cluster to 1-cluster
    decay_rate = None

    @classmethod
    def setParameters(cls, c_ch4, T = 1300+273):
        Config.c_ch4 = c_ch4
        Config.p = c_ch4 * Config.p0
        print('p:%e'%Config.p)
        Config.I = Config.p / math.sqrt(2*math.pi*Config.m*Config.k_B*T) * 1e-4
        print('I:%e'%Config.I)
        Config.k_des = Config.gamma_des0 * math.exp(-Config.e * Config.E_des / Config.k_B / T)
        print('k_des: %e' % Config.k_des)
        Config.D = Config.gamma_diff/4/Config.n0 * math.exp(-Config.e*Config.E_diff/Config.k_B/T)
        print('Diffusion coefficient:%e'%Config.D)
        Config.k_act = Config.A_const * math.exp(-Config.e * Config.E_a / Config.k_B / T)
        print('k_act:%e' % Config.k_act)
        # Config.k_deact = Config.B_const * math.exp(-Config.e*Config.E_d/Config.k_B/T)
        Config.k_deact = 0
        print('k_deact:%e' % Config.k_deact)
        Config.decay_rate = Config.gamma_decay*math.exp(-Config.e*Config.delta_E_decay/Config.k_B/T)
        print('decay:%e'%Config.decay_rate)

    # sticking coefficient as function of surface site coverage. Fitted by Ref:Li.two-step.
    @staticmethod
    def s(theta):
        # No precursor effect. Suitable for large desorption,
        return Config.sigma_ads * (1-theta)

    @staticmethod
    def s2(theta, Kp=1):
        # precursor mediated
        # assume B = 0. Precursor complete disorder. theta00 = 1 - theta
        # Kp = 1 fall back to Langmuir.
        return Config.s0/(1+Kp*theta/(1-theta))