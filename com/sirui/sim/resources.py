import simpy

class Site(object):
    def __init__(self, env, atom = None):
        self.atom = atom
        self.resource = simpy.Resource(env)

class Lattice(object):
    def __init__(self, env, atom = None):
        self.sites = [Site(env, atom), Site(env, atom)]


class Field(object):
    # Simulation Scope
    # 2D plane simple cube
    # TODO 2D plane hex
    def __init__(self, env, scope_size):
        self.env = env
        # one piece of resource for each location
        self.lattices = [[Lattice(env) for i in range(scope_size)] for j in range(scope_size)]

    def getLattice(self, position):
        return self.lattices[position.x][position.y]

    def getSite(self, position):
        return self.getLattice(position).sites[position.k]

    def isSiteOccupied(self, position):
        if self.getSite(position).resource.count == 0:
            return False
        else:
            return True

    def setSiteAtom(self, position, atom):
        self.getSite(position).atom = atom

    def requestSite(self, position):
        return self.getSite(position).resource.request()

    def getSiteAtom(self, position):
        return self.getSite(position).atom

    def releaseSite(self, position, request):
        self.getSite(position).resource.release(request)