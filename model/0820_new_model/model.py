from __future__ import division

from config import Config


###############################################
# Assume dimmer is unstable, trimer is stable.
# i = 2. i - critical cluster size.
# Assume unstable clusters take full site. Stable clusters take partial site. Due to dense phase change.
def f_rate_2(y, t):
    """
    parameter:
    y. initial value of ode.
    sigma - sticking coeff
    delta - decay rate

    variables:
    n - density (#cluster/m^2)
    n1 - adatom density. Num of adatom per unit area.
    a_s - total sites covered by stable cluster (#site/cm^2)
    a_d - total sites covered by defect induced cluster (#site/cm^2)

    """

    theta, n_CH4, n1, a2, ns, a_s, a_d = y
    sigma = Config.sigma
    sigma_s = Config.sigma_s
    delta = Config.decay_rate
    D = Config.D
    dn_CH4_dt = Config.s(theta, 0.3) * Config.I - n_CH4 * Config.k_des - Config.k_act * n_CH4 + Config.k_deact * n1
    dn1_dt = Config.k_act*n_CH4 - Config.k_deact*n1 - sigma*D*n1*(2*n1+a2) - sigma_s*D*n1*(a_s+a_d) +\
             delta*a2*2
    da2_dt = sigma*D*n1*2*n1 - sigma*D*n1*2*a2 - delta*a2*2
    dns_dt = sigma*D*n1*a2
    das_dt = (3*sigma*D*n1*a2 + sigma_s*D*n1*a_s)*Config.K
    dad_dt = sigma_s*D*n1*a_d * Config.K
    dtheta_dt = (dn_CH4_dt + dn1_dt + da2_dt + das_dt + dad_dt) / Config.n0
    return [dtheta_dt, dn_CH4_dt, dn1_dt, da2_dt, dns_dt, das_dt, dad_dt]
