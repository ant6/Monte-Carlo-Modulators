from matplotlib import use
use("Qt5Agg")  # should be called before pyplot
import matplotlib.pyplot as plt

__all__ = ["plot_one_peak"]


def plot_one_peak(peak, title=None):
    plt.clf()
    plt.xlabel("Depth in water [mm]")
    plt.ylabel("Relative dose")
    if title:
        plt.title(title)
    plt.plot(peak[0], peak[1])
    plt.show()
