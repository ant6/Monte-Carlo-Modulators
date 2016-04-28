from itertools import zip_longest
import numpy as np


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

    # single peak tests
    peak1 = read_one_peak(join("..", "data", "rs0.dat"))
    peak2 = read_one_peak(join("..", "data", "rs3000.dat"))
    peak3 = read_one_peak(join("..", "data", "rs6000.dat"))

    # uncomment to show only one peak
    # plot_one_peak(peak1)
    # plot_one_peak(peak2)
    # plot_one_peak(peak3)

    # sum different peaks at original locations to single peak
    sum = sum_peak_to_one([peak1, peak2, peak3])

    # plot sum without normalization
    # plot_one_peak(sum)

    # simple values normalization -> [0; 1]
    sum[1] /= sum[1].max()
    # plot normalized sum peak
    # plot_one_peak(sum)

    # calculate_number_of_peaks(5.0, 15.0, peak1)
    print(check_conditions(5, 15, sum))
    shifted_peak = roll_peak_to_val(peak1, 12.3)
    plot_one_peak(shifted_peak)

