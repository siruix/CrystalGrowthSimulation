from __future__ import division

from config import Config


###############################################
# Assume dimmer is unstable, trimer is stable.
# i = 2 (easiest case). i - critical cluster size.
# Assume unstable clusters take full site. Stable clusters take partial site. Due to dense phase change.
def f_rate2(y, t, para):
    """
    parameter:
    y. initial value of ode.

    variables:
    n - density (#cluster/m^2)
    n1 - adatom density. Num of adatom per unit area.
    a_s - total sites covered by stable cluster (#site/cm^2)
    a_d - total sites covered by defect induced cluster (#site/cm^2)
    sigma_1 - sticking coeff of unstable atom
    sigma_2,sigma_s,sigma_d - sticking coeff of stable cluster
    delta - decay rate
    """

    n_CH4, n1, au, ns, a_s, a_d, theta = y
    sigma_1,sigma_2,sigma_s,sigma_d,delta = para
    dn_CH4_dt = Config.s2(theta,0.3)*Config.I - n_CH4*Config.k_des - Config.k_act * n_CH4 + Config.k_deact * n1
    D = Config.D
    dn1_dt = Config.k_act*n_CH4 - Config.k_deact*n1 - 2*sigma_1*D*n1*n1 - sigma_2*D*n1*au +\
             delta*au - sigma_s*D*n1*a_s - sigma_d*D*n1*a_d
    dau_dt = 2*sigma_1*D*n1*n1 - 2*sigma_2*D*n1*au - delta*au
    dns_dt = sigma_2*D*n1*au
    das_dt = (3*sigma_2*D*n1*au + sigma_s*D*n1*a_s)*Config.K
    dad_dt = sigma_d*D*n1*a_d * Config.K
    dtheta_dt = (dn_CH4_dt + dn1_dt + dau_dt + das_dt + dad_dt) / Config.n0   # will lose count of some atom. Larger than real.
    return [dn_CH4_dt, dn1_dt, dau_dt, dns_dt, das_dt, dad_dt, dtheta_dt]
