from matplotlib import use

use("Qt5Agg")  # should be called before pyplot
import matplotlib.pyplot as plt


def plot_one_peak(peak):
    plt.clf()
    plt.xlabel("Depth in water [mm]")
    plt.ylabel("Relative dose")
    plt.plot(peak[0], peak[1])
    plt.show()
