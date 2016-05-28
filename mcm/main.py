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


def run_sim(n=None, begin='5.0', end='15.0'):
    # load peak data
    domain = read_one_peak(join("data", "domain.dat"))
    peak1_vals = read_one_peak(join("data", "rs0.dat"))
    peak2_vals = read_one_peak(join("data", "rs3000.dat"))
    peak3_vals = read_one_peak(join("data", "rs6000.dat"))
    peak4_vals = read_one_peak(join("data", "rs_weird1.dat"))
    peak5_vals = read_one_peak(join("data", "rs_weird2.dat"))

    # TODO: change this to something reasonable
    peak1 = np.array([domain, peak1_vals])
    peak2 = np.array([domain, peak2_vals])
    peak3 = np.array([domain, peak3_vals])
    peak4 = np.array([domain, peak4_vals])
    peak5 = np.array([domain, peak5_vals])
    # peak_list = [peak1, peak2, peak3, peak4, peak5]
    peak_list = [peak4, peak5]

    begin = float(begin)
    end = float(end)
    best_score = 9999
    if not n:
        # calculate mean width of peak based on our peak database (peak_list)
        temp_number_of_peaks = []
        for p in peak_list:
            temp_number_of_peaks.append(calculate_number_of_peaks(begin, end, p))
        number_of_peaks = int(np.mean(temp_number_of_peaks))
    else:
        number_of_peaks = int(n)

    prepare_plot(norm=True, begin=begin, end=end)

    time_start = time()
    while 1:
        lottery_peaks = random_peaks_with_positions(begin, end, peak_list, number_of_peaks)
        peaks_to_sum = []
        for p in lottery_peaks:
            peaks_to_sum.append(roll_peak_to_val(p[0], p[1]))

        # calculate sum peak and check condition score
        result_peak = sum_peak_to_one(peaks_to_sum)
        result_peak[1] /= (result_peak[1].max())
        score = check_conditions_with_weights(begin, end, result_peak)

        time_elapsed = time() - time_start

        print("Elapsed time: %.1fs | Current score: %.2f\r" % (time_elapsed, score), end='', flush=True)
        plot_one_peak('current', result_peak, format='k')

        if score < best_score:
            print("New best score: %.2f in %.2f seconds.   " % (score, time_elapsed))
            plot_one_peak('best', result_peak, title="Score %.4f (better by %.4f)" % (score, best_score - score), format='r')
            best_score = score
            for p in lottery_peaks:
                print("Peak with position %.2f" % (p[1], ))
            print("----------")
            time_start = time()
