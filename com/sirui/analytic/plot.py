import matplotlib.pyplot as plt
def plot(monitor, scope_size):
    for i in range(len(monitor)):
        y = [0]*len(monitor[i])
        for j, location in enumerate(monitor[i]):
            y[location] = 1
        plt.plot(range(scope_size), y, 'ro')