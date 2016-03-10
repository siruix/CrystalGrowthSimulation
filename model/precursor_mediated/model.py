from __future__ import division
from config import Config

###############################################
# rate equations i = 2
# i - cluster : critical cluster size
# assume dimmer is stable. i = 1 (easiest case)
# n1 adatom density. Num of adatom per unit area. Time dependence.

def f_rate2(y, t, para):
    # assume i=2. 3-cluster is stable
    # n - density (#cluster/m^2)
    # a_s - total sites covered by stable cluster (#site/cm^2)
    # a_d - total sites covered by defect induced cluster (#site/cm^2)
    # Assume unstable cluster takes 1 site.
    n1, n2, ns, a_s, a_d, theta = y
    sigma_1,sigma_2,sigma_s,sigma_d,delta_2 = para
    D = Config.D
    K = 0
    # - Config.k_des*n1
    dn1_dt = Config.s_precursor_mediated(theta, K)*Config.I  \
             - 2*sigma_1*D*n1*n1 - sigma_2*D*n1*n2 +\
             2*delta_2*n2 - n1*sigma_s*D*a_s - n1*sigma_d*D*a_d
    dn2_dt = sigma_1*D*n1*n1 - sigma_2*D*n1*n2 - delta_2*n2
    dns_dt = sigma_2*D*n1*n2
    das_dt = sigma_2*D*n1*n2 + sigma_s*D*n1*a_s
    dad_dt = sigma_d*D*n1*a_d
    dtheta_dt = (Config.s_precursor_mediated(theta, K) * Config.I - Config.k_des * n1) / Config.n0   # will lose count of some atom. Larger than real.
    return [dn1_dt, dn2_dt, dns_dt, das_dt, dad_dt, dtheta_dt]

def f_rate3(y, t, para):
    # n - density (#cluster/m^2)
    # a_s - total sites covered by stable cluster (#site/cm^2)
    # a_d - total sites covered by defect induced cluster (#site/cm^2)
    # Assume unstable cluster nu takes 1 site.
    n1, n2, n3, ns, a_s, a_d, theta = y
    sigma_1,sigma_2,sigma_3,sigma_s,sigma_d,delta_2,delta_3 = para
    D = Config.D
    K = 0
    dn1_dt = Config.s_precursor_mediated(theta, K)*Config.I - Config.k_des * n1 \
            - 2*sigma_1*D*n1*n1 - sigma_2*D*n1*n2 + 2*delta_2*n2 + delta_3*n3\
            - n1*sigma_3*D*n3- n1*sigma_s*D*a_s - n1*sigma_d*D*a_d
    dn2_dt = sigma_1*D*n1*n1 - sigma_2*D*n1*n2 - delta_2*n2 + delta_3*n3
    dn3_dt = sigma_2*D*n1*n2 - delta_3*n3
    dns_dt = sigma_3*D*n1*n3
    das_dt = sigma_3*D*n1*n3 + sigma_s*D*n1*a_s
    dad_dt = sigma_d*D*n1*a_d
    dtheta_dt = (Config.s_precursor_mediated(theta, K) * Config.I - Config.k_des * n1) / Config.n0   # will lose count of some atom. Larger than real.
    return [dn1_dt, dn2_dt, dn3_dt, dns_dt, das_dt, dad_dt, dtheta_dt]