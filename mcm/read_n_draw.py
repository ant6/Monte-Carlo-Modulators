from matplotlib import use
use("Qt5Agg")
import matplotlib.pyplot as plt
import numpy as np
import pickle

data = pickle.load(open("1464640516.0188088.p", "rb"))

x = np.array(data).T[0]
y = np.array(data).T[1]

plt.plot(x, y)
plt.show()
