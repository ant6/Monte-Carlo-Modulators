from os.path import join

import time

from mcm.lottery import random_positions
from mcm.measurements import roll_peak_to_val, where_is_this_val, sum_peak_to_one
from mcm.peak_reader import read_one_peak
import numpy as np


def quality(sum_peak):
    domain = sum_peak[0]
    values = sum_peak[1]
    ind_begin = where_is_this_val(begin, domain)
    ind_end = where_is_this_val(end, domain)

    pre_penalty = np.abs(values[0:ind_begin].sum())
    post_penalty = np.abs(values[ind_end:-1].sum())

    middle_sector = np.array(values[ind_begin:ind_end]) - 1
    middle_penalty = np.abs(middle_sector.sum())

    return pre_penalty + middle_penalty + post_penalty


if __name__ == '__main__':
    # load peak data
    domain = read_one_peak(join("..", "data", "domain.dat"))
    peak1_vals = read_one_peak(join("..", "data", "rs0.dat"))
    peak2_vals = read_one_peak(join("..", "data", "rs3000.dat"))
    peak3_vals = read_one_peak(join("..", "data", "rs6000.dat"))

    peak1 = np.array([domain, peak1_vals])
    peak2 = np.array([domain, peak2_vals])
    peak3 = np.array([domain, peak3_vals])

    peak_list = [peak1, peak2, peak3, peak1, peak1, peak3]

    t_start = time.time()
    k = 0
    k_end = 100000
    r = 0
    begin = 5
    end = 15
    results = []

    while k < k_end:
        k += 1

        lottery_positions = random_positions(peak_list)
        peaks_to_sum = []
        for i in range(6):
            peaks_to_sum.append(roll_peak_to_val(peak_list[i], lottery_positions[i]))

        # calculate sum peak and check condition score
        result_peak = sum_peak_to_one(peaks_to_sum)
        result_peak[1] /= (result_peak[1].max())
        qnew = quality(result_peak)
        results.append((k, qnew))

    t_end = time.time()
    print("Computed in %.2f" % (t_end - t_start))

    # dump data
    import pickle
    with open("%s.p" % time.time(), "w+b") as f:
        pickle.dump(results, f)
