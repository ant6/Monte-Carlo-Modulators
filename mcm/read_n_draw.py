from matplotlib import use
use("Qt5Agg")
import matplotlib.pyplot as plt
import numpy as np
import pickle
from os.path import join


class BullszitError(Exception):
    pass

# Annealing
data_an = pickle.load(open(join("..", "res", "1464640516.0188088.p"), "rb"))  # 10k
# data_an = pickle.load(open(join("..", "res", "1464643304.7194686.p"), "rb"))  # 1k

# Monte Carlo
# data_mc = pickle.load(open(join("..", "res", "1464709910.6499007.p"), "rb"))  # 1k
# data_mc = pickle.load(open(join("..", "res", "1464710211.0149205.p"), "rb"))  # 10k
data_mc = pickle.load(open(join("..", "res", "1464710544.9451396.p"), "rb"))  # better 10k

xa, ya = np.array(data_an).T
xm, ym = np.array(data_mc).T

if len(xa) != len(xm):
    raise BullszitError("Domains are different!")

hands = []
if data_an:
    ya2 = []
    best = ya[0]
    for e in ya:
        if e < best:
            best = e
        ya2.append(best)
    a1, = plt.plot(xa, ya, label="SA score")
    a2, = plt.plot(xa, ya2, label="SA best")
    hands.append(a1)
    hands.append(a2)

if data_mc:
    ym2 = []
    best = ym[0]
    for e in ym:
        if e < best:
            best = e
        ym2.append(best)
    m1, = plt.plot(xm, ym, label="MC score")
    m2, = plt.plot(xm, ym2, label="MC best")
    hands.append(m1)
    hands.append(m2)

plt.xlabel("Time")
plt.ylabel("Quality")
plt.legend(handles=hands)
plt.savefig("../res/10k_result.png")
plt.show()
