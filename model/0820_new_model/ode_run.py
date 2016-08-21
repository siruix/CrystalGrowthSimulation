import numpy as np
from pylab import *
import scipy.integrate as spi

def ode_run(eq_system, y0, start_t, end_t, step, *para):
    #Parameter Values
    # S0 = 99.
    # I0 = 1.
    # R0 = 0.
    # PopIn= (S0, I0, R0)
    # beta= 0.50
    # gamma=1/10.
    # mu = 1/25550.
    # t_end = 15000.
    # t_start = 1.
    # t_step = 1.
    # t_interval = np.arange(t_start, t_end, t_step)

    #Solving the differential equation. Solves over t for initial conditions PopIn
    # def eq_system(t,PopIn):
    #     '''Defining SIR System of Equations'''
    #     #Creating an array of equations
    #     Eqs= np.zeros((3))
    #     Eqs[0]= -beta * (PopIn[0]*PopIn[1]/(PopIn[0]+PopIn[1]+PopIn[2])) - mu*PopIn[0] + mu*(PopIn[0]+PopIn[1]+PopIn[2])
    #     Eqs[1]= (beta * (PopIn[0]*PopIn[1]/(PopIn[0]+PopIn[1]+PopIn[2])) - gamma*PopIn[1] - mu*PopIn[1])
    #     Eqs[2]= gamma*PopIn[1] - mu*PopIn[2]
    #     return Eqs

    ode =  spi.ode(eq_system)

    # BDF method suited to stiff systems of ODEs
    ode.set_integrator('vode',nsteps=1000000,method='bdf')
    ode.set_initial_value(y0, start_t)
    ode.set_f_params(*para)

    ts = []
    ys = []
    while ode.successful() and ode.t < end_t:
        ode.integrate(ode.t + step)
        ts.append(ode.t)
        ys.append(ode.y)

    # t = np.vstack(ts)
    # s,i,r =

    # fig,ax = subplots(1,1)
    # ax.hold(True)
    # ax.plot(t,s,label='Susceptible')
    # ax.plot(t,i,label='Infected')
    # ax.plot(t,r,label='Recovered')
    # ax.set_xlim(t_start,t_end)
    # ax.set_ylim(0,100)
    # ax.set_xlabel('Time')
    # ax.set_ylabel('Percent')
    # ax.legend(loc=0,fancybox=True)

    return np.vstack(ys).T