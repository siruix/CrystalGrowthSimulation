import simpy
class Site(object):
    def __init__(self, env, atom = None):
        self.resource = simpy.Resource(env)
        self.atom = atom

class Field(object):
    # Simulation Scope
    # 2D plane simple cube
    # TODO 2D plane hex
    def __init__(self, env, scope_size):
        self.env = env
        # one piece of resource for each location
        self.sites = [[Site(env) for i in range(scope_size)] for j in range(scope_size)]

    def getSite(self, position):
        return self.sites[position.x][position.y]