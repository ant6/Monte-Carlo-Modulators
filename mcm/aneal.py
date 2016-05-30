from os.path import join
from mcm.measurements import roll_peak_to_val, where_is_this_val, sum_peak_to_one
from mcm.peak_reader import read_one_peak
import numpy as np
import random


def _plot_one_peak(peak, title=None):
    if title:
        plt.title(title)
    plt.plot(peak[0], peak[1])
    plt.show()


class PeakSet:
    def __init__(self, peaks, positions):
        self.peaks = peaks
        self.positions = positions
        self.begin = 5.0
        self.end = 20.0

    def sum_peak(self):
        sum_peak = sum_peak_to_one(self.peaks)
        sum_peak[1] /= (sum_peak[1].max())
        return sum_peak

    def quality(self):
        sum = self.sum_peak()
        domain = sum[0]
        values = sum[1]
        ind_begin = where_is_this_val(self.begin, domain)
        ind_end = where_is_this_val(self.end, domain)

        pre_penalty = np.abs(values[0:ind_begin].sum())
        post_penalty = np.abs(values[ind_end:-1].sum())

        middle_sector = np.array(values[ind_begin:ind_end]) - 1
        middle_penalty = np.abs(middle_sector.sum())

        return (pre_penalty * 0.2) + (middle_penalty * 0.8) + (post_penalty * 0.1)

    def randomly_move(self):
        new_pos = []
        new_peaks = []
        for pos in self.positions:
            pos += random.uniform(-1, 1)
            new_pos.append(pos)
        self.positions = new_pos

        i = 0
        for peak in self.peaks:
            new_peaks.append(roll_peak_to_val(peak, self.positions[i]))
            i += 1
        self.peaks = new_peaks

    def begin(self, b):
        self.begin = b

    def end(self, e):
        self.end = e


if __name__ == '__main__':
    from matplotlib import use
    use("Qt5Agg")
    import matplotlib.pyplot as plt
    # load peak data
    domain = read_one_peak(join("..", "data", "domain.dat"))
    peak1_vals = read_one_peak(join("..", "data", "rs0.dat"))
    peak2_vals = read_one_peak(join("..", "data", "rs3000.dat"))
    peak3_vals = read_one_peak(join("..", "data", "rs6000.dat"))
    peak4_vals = read_one_peak(join("..", "data", "rs_weird1.dat"))
    peak5_vals = read_one_peak(join("..", "data", "rs_weird2.dat"))

    peak1 = np.array([domain, peak1_vals])
    peak2 = np.array([domain, peak2_vals])
    peak3 = np.array([domain, peak3_vals])
    peak4 = np.array([domain, peak4_vals])
    peak5 = np.array([domain, peak5_vals])
    # peak_list = [peak1, peak2, peak3, peak4, peak5]
    peak_list = [peak1, peak2, peak3]

    k = 0
    k_end = 1000

    p = PeakSet(peak_list, [5, 8, 12])

    while k < k_end:
        k += 1
        temp = k/k_end
        p.randomly_move()
        en = p.quality()
        print(k, en)

        _plot_one_peak(p.sum_peak())
