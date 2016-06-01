from matplotlib import use
use("Qt5Agg")
import matplotlib.pyplot as plt
from os.path import join
import numpy as np

from mcm.peak_reader import read_one_peak

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
peak_list = [peak1, peak2, peak3, peak4, peak5]

for p in peak_list:
    plt.plot(p[0], p[1])

plt.xlabel("Zasieg [mm]")
plt.ylabel("Dawka")
# plt.show()
plt.savefig("gorki")
