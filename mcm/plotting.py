import logging
import numpy as np
from matplotlib import use
use("Qt5Agg")  # should be called before pyplot
import matplotlib.pyplot as plt

__all__ = ["prepare_plot", "plot_one_peak"]


plots = {}


def prepare_plot(norm=True, begin=None, end=None):
    plt.ion()
    plt.xlabel("Depth in water [mm]")
    plt.ylabel("Relative dose")
    if norm:
        plt.ylim([0, 1.2])
    if begin and end:
        plt.plot([begin, begin], [0, 1.2])
        plt.plot([end, end], [0, 1.2])
        plt.grid(True)
    plt.show()


def plot_one_peak(name, peak, title=None, format=''):
    if title:
        plt.title(title)
    try:
        plots[name].remove()
    except KeyError:
        pass
    plots[name], = plt.plot(peak[0], peak[1], format)
    plt.pause(0.001)


def do_some_magic(sum_peak, begin, end):
    # profile
    domain = sum_peak[0]
    values = sum_peak[1]
    middle = (begin + end) / 2
    width = end - begin
    logging.debug("approx middle = %f\napprox width = %f" % (middle, width))
    section = [middle - width / 4, middle + width / 4]
    section_coords = [(np.abs(domain - section[0])).argmin(),
                      (np.abs(domain - section[1])).argmin()]
    norm = np.mean(values[section_coords[0]:section_coords[1]])
    logging.debug("Calculated norm = %f" % norm)
    values /= norm

    # draw plots
    plt.plot(domain, values)
    plt.plot((0, domain[-1]), (1.04, 1.04))
    plt.plot((0, domain[-1]), (1.02, 1.02))
    plt.plot((0, domain[-1]), (1, 1))
    plt.plot((0, domain[-1]), (0.98, 0.98))
    plt.plot((0, domain[-1]), (0.96, 0.96))
    plt.xlim([0, domain[-1]])
    plt.show()
    plt.clf()
