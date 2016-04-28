from time import time

import numpy as np
import logging
from os.path import join

from mcm.lottery import random_peaks_with_positions
from mcm.measurements import *
from mcm.plotting import *
from mcm.peak_reader import *

logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] %(pathname)s at line %(lineno)s (function: %(funcName)s)\n%(message)s\n")


def run_sim():
    # load peak data
    domain = read_one_peak(join("data", "domain.dat"))
    peak1_vals = read_one_peak(join("data", "rs0.dat"))
    peak2_vals = read_one_peak(join("data", "rs3000.dat"))
    peak3_vals = read_one_peak(join("data", "rs6000.dat"))

    # TODO: change this temporary fix to something reasonable
    peak1 = np.array([domain, peak1_vals])
    peak2 = np.array([domain, peak2_vals])
    peak3 = np.array([domain, peak3_vals])
    peak_list = [peak1, peak2, peak3]

    # TODO: median filter to make values more smooth?

    begin = 5.0
    end = 15.0
    best_score = 0.0
    number_of_peaks = (calculate_number_of_peaks(begin, end, peak1))

    time_start = time()
    while 1:
        lottery_peaks = random_peaks_with_positions(begin, end, peak_list, number_of_peaks)
        peaks_to_sum = []
        for p in lottery_peaks:
            peaks_to_sum.append(roll_peak_to_val(p[0], p[1]))

        # calculate sum peak and check condition score
        result_peak = sum_peak_to_one(peaks_to_sum)
        result_peak[1] /= result_peak[1].max()
        score = check_conditions(begin, end, result_peak)

        if score > best_score:
            time_elapse = time()
            print("New best score: %.2f in %.2f seconds." % (score, time_elapse - time_start))
            plot_one_peak(result_peak, title="Score %.4f (better %.4f)" % (score, score - best_score), norm=True, begin=begin, end=end)
            best_score = score
            for p in lottery_peaks:
                print("Peak with position %.2f" % (p[1]))
            print("----------")
            time_start = time()
