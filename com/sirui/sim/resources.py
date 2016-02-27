import simpy
from com.sirui.sim.config import Config
from com.sirui.sim.position import Position
# Simple Cube Lattice (100) face
# Atoms are permitted only at sc lattice site
# One atom only allowed to occupy a site
# Only consider nearest neighbor interactions
class Site(object):
    def __init__(self, env, atom = None):
        self.atom = atom
        self.resource = simpy.Resource(env)

class Lattice(object):
    # Each lattice may have more than one site. Here consider only one.
    def __init__(self, env, atom = None):
        self.sites = [Site(env, atom), Site(env, atom)]


class Field(object):
    # Simulation Scope
    # 3D plane simple cube
    def __init__(self, env, scope_size):
        self.env = env
        # one piece of resource for each location
        # the z dimension height is fixed. If exceeding, ignored.
        self.lattices = [[[Lattice(env) for i in range(scope_size)] for j in range(scope_size)] for k in range(Config.SCOPE_HEIGHT)]

    def getLattice(self, position):
        return self.lattices[position.z][position.y][position.x]

    def getSite(self, position):
        return self.getLattice(position).sites[position.k]

    def isSiteOccupied(self, position):
        if self.getSite(position).resource.count == 0:
            return False
        else:
            return True

    def isSurface(self, position):
        if not self.isSiteOccupied(Position(position.x, position.y, position.z+1)):
            return True
        else:
            return False

    def setSiteAtom(self, position, atom):
        self.getSite(position).atom = atom

    def requestSite(self, position):
        return self.getSite(position).resource.request()

    def getSiteAtom(self, position):
        return self.getSite(position).atom

    def releaseSite(self, position, request):
        self.getSite(position).resource.release(request)

    def getLowestUnoccupiedPosition(self, x, y):
        for z in range(Config.SCOPE_HEIGHT):
            if not self.isSiteOccupied(Position(x, y, z)):
                return Position(x, y, z)
        return None