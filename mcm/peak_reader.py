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
    start = 5.0
    stop = 15.0

    from os.path import join
    peak = read_one_peak(join("..", "data", "rs0.dat"))
    print(peak)
    from mcm.measurements import calculate_number_of_peaks
    calculate_number_of_peaks(5.0, 15.0, peak)
