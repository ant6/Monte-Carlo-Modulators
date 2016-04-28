import numpy as np
import logging
from os.path import join
from mcm.measurements import *
from mcm.plotting import *
from mcm.peak_reader import *

logging.basicConfig(level=logging.DEBUG,
                    format="[%(levelname)s] %(pathname)s at line %(lineno)s (function: %(funcName)s)\n%(message)s\n")


if __name__ == '__main__':
    # load peak data
    domain = read_one_peak(join("..", "data", "domain.dat"))
    peak1_vals = read_one_peak(join("..", "data", "rs0.dat"))
    peak2_vals = read_one_peak(join("..", "data", "rs3000.dat"))
    peak3_vals = read_one_peak(join("..", "data", "rs6000.dat"))

    # TODO: change this temporary fix to something reasonable
    peak1 = np.array([domain, peak1_vals])
    peak2 = np.array([domain, peak2_vals])
    peak3 = np.array([domain, peak3_vals])

    # TODO: median filter to make values more smooth?

    # uncomment to show only one peak
    # plot_one_peak(peak1)
    # plot_one_peak(peak2)
    # plot_one_peak(peak3)

    # sum different peaks at original locations to single peak
    a = roll_peak_to_val(peak3, 22)
    b = roll_peak_to_val(peak2, 24)
    c = roll_peak_to_val(peak1, 26)
    d = roll_peak_to_val(peak1, 28)
    sum = sum_peak_to_one([a, b, c, d])

    # plot sum without normalization
    # plot_one_peak(sum, norm=False)

    # simple values normalization -> [0; 1]
    sum[1] /= sum[1].max()
    # plot normalized sum peak
    plot_one_peak(sum, "Sum")

    logging.info("Check conditions result = %s" % check_conditions(20, 29, sum))
    shifted_peak = roll_peak_to_val(peak1, 9.3)
    plot_one_peak(shifted_peak, "Shifted peak (%s)" % 9.3)
