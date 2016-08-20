from __future__ import division

from config import Config


###############################################
# rate equations i = 2
# i - cluster : critical cluster size
# assume dimmer is stable. i = 1 (easiest case)
# n1 adatom density. Num of adatom per unit area. Time dependence.
#
def f_rate2(y, t, para):
    # n - density (#cluster/m^2)
    # a_s - total sites covered by stable cluster (#site/cm^2)
    # a_d - total sites covered by defect induced cluster (#site/cm^2)
    # Assume unstable cluster takes 1 site.
    n_CH4, n1, n2, nx, a_s, a_d, theta = y
    sigma_1,sigma_2,sigma_s,sigma_d,delta_2 = para
    dn_CH4_dt = Config.s2(theta,1)*Config.I - n_CH4*Config.k_des - Config.k_act * n_CH4 + Config.k_deact * n1
    dn1_dt = Config.k_act*n_CH4 - Config.k_deact * n1 - 2 * sigma_1 * Config.D * n1 * n1 - sigma_2 * Config.D * n1 * n2 +\
             2*delta_2*n2 - n1*sigma_s*Config.D*a_s - n1*sigma_d*Config.D*a_d
    dn2_dt = sigma_1*Config.D*n1*n1 - sigma_2*Config.D*n1*n2 - delta_2*n2
    dns_dt = sigma_2*Config.D*n1*n2
    das_dt = sigma_2*Config.D*n1*n2 + sigma_s*Config.D*n1*a_s
    dad_dt = sigma_d*Config.D*n1*a_d
    dtheta_dt = Config.k_act * n_CH4 / Config.n0   # will lose count of some atom. Larger than real.
    return [dn_CH4_dt, dn1_dt, dn2_dt, dns_dt, das_dt, dad_dt, dtheta_dt]
