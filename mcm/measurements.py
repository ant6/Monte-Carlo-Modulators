from math import ceil
import numpy as np
from scipy.ndimage import shift

__all__ = ["calculate_number_of_peaks", "sum_peak_to_one", "check_conditions", "roll_peak_to_val"]


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


def sum_peak_to_one(peaks):
    if len(peaks) > 1:
        sum = np.zeros(len(peaks[0][0]))
        for p in peaks:
            sum += p[1]
        return np.array([peaks[0][0], sum])
    else:
        raise ValueError("Nothing to sum")


def where_is_this_val(val, one_dim_array):
    """Wrapper for numpy.where - return just one, first val found"""
    return np.where(one_dim_array == val)[0][0]


def check_conditions(begin, end, sum_peak):
    """
    We want to maximize this result (get result closest to 1)
    """
    domain = sum_peak[0]
    values = sum_peak[1]
    ind_begin = where_is_this_val(begin, domain)
    ind_end = where_is_this_val(end, domain)
    print(ind_begin, domain[ind_begin], ind_end, domain[ind_end])
    max_val = np.argmax(values)
    print(values[ind_begin], values[ind_end], max_val, values[max_val])
    # TODO: more complex condition checking
    interesting_part = values[ind_begin:ind_end]
    return 1 - (interesting_part.max() - interesting_part.min())


def roll_peak_to_val(peak, target_val):
    domain = peak[0]
    values = peak[1]
    target_ind = (np.abs(values - target_val)).argmin()
    print(target_ind)
    max_peak_val_ind = np.argmax(values)
    shift(values, -(max_peak_val_ind - target_ind), mode='nearest')
    return np.array([domain, values])
