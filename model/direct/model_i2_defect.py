from __future__ import division

from config import Config


###############################################
# rate equations. i = 1
# i - cluster : critical cluster size
# assume dimmer is stable. i = 1 (easiest case)
# n1 adatom density. Num of adatom per unit area. Time dependence.
#
# def f_rate1(y, t, para):
#     n_CH4, n1, nx, theta = y
#     sigma1, sigmax = para
#     # theta = (n_CH4 + n1 + nx)/n0
#     dn_CH4_dt = s(theta) * I - n_CH4/tau_CH4 - k_a*n_CH4 + k_d*n1
#     dn1_dt = k_a*n_CH4 - k_d*n1 - 2*sigma1*D*math.pow(n1,2) - n1*sigmax*D*nx
#     dnx_dt = math.pow(n1,2)*sigma1*D
#     dtheta_dt = (s(theta) * I - n_CH4/tau_CH4)/n0
#     return [dn_CH4_dt, dn1_dt, dnx_dt, dtheta_dt]

###############################################
# rate equations i = 2
# i - cluster : critical cluster size
# assume dimmer is stable. i = 1 (easiest case)
# n1 adatom density. Num of adatom per unit area. Time dependence.
#
def f_rate2(y, t, para):
    # n - density (#cluster/m^2)
    # ax - total sites covered by stable cluster (#site/cm^2)
    # ad - total sites covered by defect induced cluster (#site/cm^2)
    # Assume unstable cluster takes 1 site.
    n_CH4, n1, n2, nx, ax, ad, theta = y
    sigma_1,sigma_2,sigma_x,sigma_d,delta_2 = para
    dn_CH4_dt = Config.s(theta)*Config.I - n_CH4*Config.gamma_des - Config.k_a*n_CH4 + Config.k_d*n1
    dn1_dt = Config.k_a*n_CH4 - Config.k_d*n1 - 2*sigma_1*Config.D*n1*n1 - sigma_2*Config.D*n1*n2 +\
             2*delta_2*n2 - n1*sigma_x*Config.D*ax - n1*sigma_d*Config.D*ad
    dn2_dt = sigma_1*Config.D*n1*n1 - sigma_2*Config.D*n1*n2 - delta_2*n2
    dnx_dt = sigma_2*Config.D*n1*n2
    dax_dt = sigma_2*Config.D*n1*n2 + sigma_x*Config.D*n1*ax
    dad_dt = sigma_d*Config.D*n1*ad
    dtheta_dt = (Config.s(theta)*Config.I - n_CH4*Config.gamma_des)/Config.n0   # will lose count of some atom. Larger than real.
    return [dn_CH4_dt, dn1_dt, dn2_dt, dnx_dt, dax_dt, dad_dt, dtheta_dt]

def f_rate3(y, t, para):
    # n - density (#cluster/m^2)
    # ax - total sites covered by stable cluster (#site/cm^2)
    # ad - total sites covered by defect induced cluster (#site/cm^2)
    # Assume unstable cluster takes 1 site.
    n_CH4, n1, n2, nx, ax, ad, theta = y
    sigma_1,sigma_2,sigma_x,sigma_d,delta_2 = para
    dn_CH4_dt = Config.s(theta)*Config.I - n_CH4*Config.gamma_des - Config.k_a*n_CH4 + Config.k_d*n1
    dn1_dt = Config.k_a*n_CH4 - Config.k_d*n1 - 2*sigma_1*Config.D*n1*n1 - sigma_2*Config.D*n1*n2 +\
             2*delta_2*n2 - n1*sigma_x*Config.D*ax - n1*sigma_d*Config.D*ad
    dn2_dt = sigma_1*Config.D*n1*n1 - sigma_2*Config.D*n1*n2 - delta_2*n2
    dnx_dt = sigma_2*Config.D*n1*n2
    dax_dt = sigma_2*Config.D*n1*n2 + sigma_x*Config.D*n1*ax
    dad_dt = sigma_d*Config.D*n1*ad
    dtheta_dt = (Config.s(theta)*Config.I - n_CH4*Config.gamma_des)/Config.n0   # will lose count of some atom. Larger than real.
    return [dn_CH4_dt, dn1_dt, dn2_dt, dnx_dt, dax_dt, dad_dt, dtheta_dt]