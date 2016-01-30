import simpy
class Location(object):
    def __init__(self, env, atom = None):
        self.resource = simpy.Resource(env)
        self.atom = atom

class Field(object):
    def __init__(self, env, scope_size):
        self.env = env
        # one piece of resource for each location
        self.locations = [Location(env) for i in range(scope_size)]