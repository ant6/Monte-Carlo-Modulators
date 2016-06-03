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
# data_mc = pickle.load(open(join("..", "res", "1464865217.9277039.p"), "rb"))  # 100k

xa, ya = np.array(data_an).T
xm, ym = np.array(data_mc).T

fig = plt.figure()
ax = fig.add_subplot(111)

ax.annotate('Start %.f' % ya[0], xy=(0, ya[0]), xytext=(1250, 1000), arrowprops=dict(facecolor='black'))

hands = []
if data_an:
    ya2 = []
    best = ya[0]
    for e in ya:
        if e < best:
            best = e
        ya2.append(best)
    a1, = ax.plot(xa, ya, label="SA score")
    a2, = ax.plot(xa, ya2, label="SA best")
    hands.append(a1)
    hands.append(a2)
    ax.annotate('End SA %.f' % ya2[-1], xy=(xa[-1], ya2[-1]), xytext=(7500, 440), arrowprops=dict(facecolor='black'))

if data_mc:
    ym2 = []
    best = ym[0]
    for e in ym:
        if e < best:
            best = e
        ym2.append(best)
    # m1, = plt.plot(xm, ym, label="MC score")
    m2, = ax.plot(xm, ym2, label="MC best")
    # hands.append(m1)
    hands.append(m2)
    ax.annotate('End MC %.f' % ym2[-1], xy=(xm[-1], ym2[-1]), xytext=(8000, 900), arrowprops=dict(facecolor='black'))

from scipy.signal import medfilt
ym = medfilt(ym, kernel_size=21)
m1, = ax.plot(xm, ym, label="MC score")
hands.append(m1)


plt.xlabel("Time")
plt.ylabel("Quality")
ax.legend(handles=hands)
# plt.savefig("../res/10k_result.png")
plt.show()
