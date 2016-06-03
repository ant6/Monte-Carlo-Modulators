from matplotlib import use
use("Qt5Agg")
import matplotlib.pyplot as plt
import pickle
from os.path import join


def _plot_one_peak(peak, title=None):
    if title:
        plt.title(title)
    plt.ylabel("Relative dose")
    plt.xlabel("Range [mm]")
    plt.ylim([0, 1])

    plt.plot([5, 5], [1, 0])
    plt.plot([15, 15], [1, 0])

    plt.plot(peak[0], peak[1])
    plt.show()


# s = pickle.load(open(join("..", "res", "start_sa.p"), "rb"))
# b = pickle.load(open(join("..", "res", "best_sa.p"), "rb"))
b = pickle.load(open(join("..", "res", "best_mc.p"), "rb"))

# _plot_one_peak(s[0], "Starting peak set, desired range 5-15")
# _plot_one_peak(b[-1], "Best SA peak set, desired range 5-15")
_plot_one_peak(b[-1], "Best MC peak set, desired range 5-15")
