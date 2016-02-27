This file is distributed under the terms of the GNU General Public License, see http://www.gnu.org/copyleft/gpl.txt for details.
Author: Sirui Xing
Email: sirui.xing@gmail.com

What is CrystalGrowthSimulation?
The project was stemming from a course assignment of Thin Film Technique that taught by Dr. John C. Wolfe in 2012. Four years latter, as I am fighting my dissertation, I re-write all the code using Python. From my academic experience, there is a need of a simple crystal growth simulator that students can play with while learning related knowledge in the thin film area. So I decide to release the CrystalGrowthSimulation project, that anyone can build on top of it a crystal growth model without reinventing the wheel.

Dependencies?
The software depends on two core modules. One is the event-based simulation engine, simpy. The other is a 3D visualization module, VPython.
The dependencies I use:
Python 2.7.10
Simpy 3.0.8
VPython 6.11

How to use?
Simulator interface through file com.sirui.analytic.driver.py
where some parameters need to be specified. E.g. delta_mu, phi.
Simulator generates log files that tracking atom's movement under directory com.sirui.analytic.logs
The generated log files have names correspond to driver's input parameters.
Then execute file com.sirui.analytic.display.py with the same parameters as the driver.
If everything work, a 3D graphic should shows up.

Which model?
The project uses kinetic monte carlo method. It assume molecules or atoms are classical particles. Atoms are permitted only at lattice sites. Only one atom is allowed to occupy a site. Atom interacts with only its nearest neighbors.
The purpose of this project is to provide a starting point to explore different models. Here I listed the models that the project used.
Simple Cube (SC) lattice. One atom per lattice site. Dynamics of crystal growth are simulated by three basic event, adsorption, desorption, diffusion.

