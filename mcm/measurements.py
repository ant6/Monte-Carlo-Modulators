from math import ceil
import numpy as np


def calculate_peak_width(peak):
    maximum = peak[1].max()
    value = 0.8 * maximum

    vals = get_positions_of_value(peak, value)

    return vals


def get_positions_of_value(peak, value):
    pos = np.where(peak[1] == value)
    if len(pos[0]) > 0:
        return pos[0][0]
    else:
        raise ValueError()


def calculate_number_of_peaks(begin, end, peak):
    # TODO: correct this BS...
    width = calculate_peak_width(peak)

    a = np.where(peak[0] == begin)[0][0]
    b = np.where(peak[0] == end)[0][-1]

    print(a, b, b-a, width)
    number_of_peaks = 1 + int(ceil((b - a) / width))
    print(number_of_peaks)

    return number_of_peaks
