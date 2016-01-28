class Monitor(object):
    def __init__(self, sim_time, num_atom):
        self.data = [[-1 for i in range(num_atom)] for j in range(sim_time)]