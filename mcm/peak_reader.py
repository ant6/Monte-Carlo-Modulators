from itertools import zip_longest
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="[%(levelname)s] %(pathname)s at line %(lineno)s (function: %(funcName)s)\n%(message)s\n")


def transposed(matrix):
    """Return transposed matrix (list of lists).

    This function can handle non-square matrices.
    In this case it fills shorter list with None.

    >>> transposed( [[1,2,3], [3,4]] )
    [[1, 3], [2, 4], [3, None]]
    """
    return list(map(list, zip_longest(*matrix)))


def read_peak_database(peak_file):
    """
    First line of given file is treated as labels
    and is ignored.
    """

    with open(peak_file, 'r') as pf:
        splitcols = transposed([line.split() for line in pf.readlines()])

    peak_list = []
    cols = len(splitcols)  # number of columns
    for i in range(0, cols, 2):
        # deleting Nones (see transposed()) and label in the first line
        peak_domain = np.array([float(l) for l in splitcols[i][1:] if l])  # else 0.0 or np.nan?
        peak_values = np.array([float(l) for l in splitcols[i + 1][1:] if l])
        peak = np.array([peak_domain, peak_values])
        peak_list.append(peak.T)

    return np.array(peak_list)


def read_one_peak(f):
    return np.loadtxt(f, delimiter=',', unpack=True)

if __name__ == '__main__':
    from mcm.measurements import *
    from mcm.plotting import *
    from os.path import join

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
