from os.path import join

import time

from mcm.measurements import roll_peak_to_val, where_is_this_val, sum_peak_to_one
from mcm.peak_reader import read_one_peak
import numpy as np
import random
import math


best_qual = 4000000000
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


def _plot_one_peak(peak, title=None):
    if title:
        plt.title(title)
    plt.plot(peak[0], peak[1])
    plt.show()


class PeakSet:
    def __init__(self, peaks, positions):
        self.peaks = peaks
        self.positions = positions
        self._begin = 5.0
        self._end = 15.0
        self.old_positions = positions

    def sum_peak(self):
        sum_peak = sum_peak_to_one(self.peaks)
        sum_peak[1] /= (sum_peak[1].max())
        return sum_peak

    def quality(self):
        sum = self.sum_peak()
        domain = sum[0]
        values = sum[1]
        ind_begin = where_is_this_val(self._begin, domain)
        ind_end = where_is_this_val(self._end, domain)

        pre_penalty = np.abs(values[0:ind_begin].sum())
        post_penalty = np.abs(values[ind_end:-1].sum())

        middle_sector = np.array(values[ind_begin:ind_end]) - 1
        middle_penalty = np.abs(middle_sector.sum())

        return pre_penalty + middle_penalty + post_penalty

    def anneal(self):
        new_pos = []
        new_peaks = []
        for pos in self.positions:
            pos += random.uniform(-1, 1)
            new_pos.append(pos)
        self.old_positions = self.positions
        self.positions = new_pos

        i = 0
        for peak in self.peaks:
            new_peaks.append(roll_peak_to_val(peak, self.positions[i]))
            i += 1
        self.peaks = new_peaks

    def begin(self, b):
        self._begin = b

    def end(self, e):
        self._end = e

    def revert_positions(self):
        self.positions = self.old_positions


def prob_old(pre, post, t):
    if post < pre:
        return random.uniform(-t, t)
    else:
        return random.uniform(-t, 0.5 * t)


def prob(pre, post, t):
    delt = pre - post
    try:
        return math.exp(delt / t)
    except OverflowError:
        return float('inf')


if __name__ == '__main__':
    from matplotlib import use
    use("Qt5Agg")
    import matplotlib.pyplot as plt

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
    k_end = 1000
    r = 0
    begin = 5
    end = 15
    p = PeakSet(peak_list, [6, 7, 8, 9, 10, 11])
    p.begin(begin)
    p.end(end)
    results = []
    test_peaks = []
    best_peaks = []

    while k < k_end:
        k += 1
        if k < 10:
            test_peaks.append(p.sum_peak())
            print('test', len(test_peaks))
        temp = k / k_end
        e0 = p.quality()
        p.anneal()
        e1 = p.quality()
        if prob(e0, e1, temp) < random.uniform(0, 1):
            results.append((k, e0))
            p.revert_positions()
            r += 1
        else:
            results.append((k, e1))

        qual = p.quality()
        # plot_one_peak('current', p.sum_peak(), format='k')

        if qual < best_qual:
            # plot_one_peak('best', p.sum_peak(), title="Quality %.4f (better by %.4f)" % (qual, best_qual - qual), format='r')
            best_qual = qual
            best_peaks.append(p.sum_peak())
            print('best', len(best_peaks))

        if k % 100 == 0:
            print("Step: %d, sample score: %.2f" % (k, e1))
            # _plot_one_peak(p.sum_peak())

    # print time elapsed
    print("reverted %s times (ran %s times)" % (r, k_end))
    print(p.quality())

    t_end = time.time()
    print("Computed in %.2f" % (t_end - t_start))

    import pickle
    with open("sa.p", "w+b") as f:
        pickle.dump(results, f)

    with open("start_sa.p", "w+b") as f2:
        pickle.dump(test_peaks, f2)

    with open("best_sa.p", "w+b") as f3:
        pickle.dump(best_peaks, f3)
