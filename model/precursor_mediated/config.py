from __future__ import division
import math

class Config(object):

    # define experiment parameters
    # CH4 concentration
    c_ch4 = 20e-6
    # Environment temperature in K
    T = 1000 + 273

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
    p = c_ch4 * p0
    # CH4 mass per molecular in kg
    m = 16.04e-3 / Na
    # impingement. molecular per second per square-centimeter
    I = p / math.sqrt(2*math.pi*m*k_B*T)

    #############################################
    # Adsorption: CH4(g) -> CH4(p) -> CHx(a)
    # Precursor mediated adsorption
    # initial sticking coefficient at phi=0
    s0 = 1
    # see static method

    #############################################
    # Desorption: CH4(g) <- CH4(p) <- CHx(a)
    # atomic frequency of crystal lattice
    gamma_des_0 = 1e13
    # energy barrier to desorb in eV. Larger, the more CHx accumulation
    E_des = 0.7#0.7
    # rate of desorb of CHx(a)
    # k_des = gamma_des_0 * math.exp(-e * E_des / k_B / T)
    k_des = gamma_des_0 * 1e-5
    print('k_des:%e' % k_des)
    #############################################
    # Diffusion
    # energy barrier to diffuse for CHx in eV
    E_diff = 0.1 # a guess. typically 5-20% of E_d
    # Diffusion pre-factor. Larger the longer diffusion
    # oscillation frequency of atom. Attempt frequency to overcome barrier.
    gamma_diff = 1e13 #?
    # adsorption site spacing in centimeter
    a = 3.615e-8 #? lattice space
    # adsorption site per unit area
    n0 = 1 / math.pow(a, 2)
    print('n0:%e'%n0)
    # Diffusion of CHx in unit area per second
    D = gamma_diff/4/n0 * math.exp(-e*E_diff/k_B/T)
    print('Diffusion:%e'%D)
    ############################################
    # Defect
    # defect site per unit area
    nd = n0 * 0 #1e-13
    ############################################
    # # CH4 to CHx activation energy barrier in eV
    # E_a = 2.51 # ref: First-principle
    # # coefficient. Larger the more CHx
    # A_const = 7e11
    # # reaction rate CH4 to CHx
    # k_a = A_const * math.exp(-e*E_a/k_B/T)
    # print('ka:%e'%k_a)
    # # CHx to CH4 activation energy barrier in eV
    # E_d = 0.65 # ref: First-principle
    # # coefficient. Smaller the more CHx, the more nucleation
    # B_const = 1e-2#?
    # # reaction rate CHx to CH4
    # k_d = B_const * math.exp(-e*E_d/k_B/T)
    # print('kd:%e'%k_d)
    ############################################
    # decay rate coefficient. Attempt frequency decay.
    gamma_decay = 1e13
    # energy difference between 2-cluster and 1-cluster (eV). Larger the faster decay.
    delta_E_decay = 0.95 #larger the slower decay. More nucleation. Start time same.
    # decay rate from 2-cluster to 1-cluster
    decay_rate = gamma_decay * math.exp(-e * delta_E_decay / k_B / T)
    print('decay:%e'%decay_rate)

    @classmethod
    def set_parameters(cls, c_ch4):
        Config.c_ch4 = c_ch4
        Config.p = c_ch4 * Config.p0
        Config.I = Config.p / math.sqrt(2*math.pi*Config.m*Config.k_B*Config.T)
        print('I:%e'%Config.I)
    # sticking coefficient as function of surface site coverage. Fitted by Ref:Li.two-step.
    @staticmethod
    def s(theta):
        # num atom adsorb per unit time per unit area as function of surface site coverage
        return Config.s0 * (1 - theta)

    @staticmethod
    def s_precursor_mediated(theta, K, n=1):
        t = (1 - theta) ** n
        # return Config.s0*(1+K)*t / (1 + K*t)
        return Config.s0*(1-theta)