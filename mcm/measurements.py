import logging
from math import ceil
import numpy as np
from scipy.ndimage import shift

__all__ = ["calculate_number_of_peaks", "sum_peak_to_one", "check_conditions", "roll_peak_to_val"]


def calculate_peak_width(peak):
    maximum = peak[1].max()
    value = 0.75 * maximum
    vals = np.where(peak[1] == value)

    return vals[0][-1] - vals[0][0]


def calculate_number_of_peaks(begin, end, peak):
    # TODO: correct this BS...
    width_in_ind = calculate_peak_width(peak)

    begin_ind = where_is_this_val(begin, peak[0])
    end_ind = where_is_this_val(end, peak[0])

    print(begin_ind, end_ind, end_ind-begin_ind, width_in_ind)
    number_of_peaks = 1 + int(ceil((end_ind - begin_ind) / width_in_ind))

    return number_of_peaks


def sum_peak_to_one(peaks):
    if len(peaks) > 1:
        peak_sum = np.zeros(len(peaks[0][0]))
        for p in peaks:
            peak_sum += p[1]
        return np.array([peaks[0][0], peak_sum])
    else:
        raise ValueError("Nothing to sum")


def where_is_this_val(val, one_dim_array):
    """Wrapper for numpy.where - return just one, first val found"""
    return (np.abs(one_dim_array - val)).argmin()


def check_conditions(begin, end, sum_peak):
    """
    We want to maximize this result (get result closest to 1)
    """
    domain = sum_peak[0]
    values = sum_peak[1]
    ind_begin = where_is_this_val(begin, domain)
    ind_end = where_is_this_val(end, domain)
    # TODO: more complex condition checking
    interesting_part = values[ind_begin:ind_end]
    return 1 - (interesting_part.max() - interesting_part.min())


def roll_peak_to_val(peak, target_val):
    domain = peak[0]
    values = peak[1]
    target_ind = (np.abs(domain - target_val)).argmin()
    max_peak_val_ind = np.argmax(values)
    logging.debug("Target shift index = %s\nMax peak value index = %s" % (target_ind, max_peak_val_ind))
    values = shift(values, -(max_peak_val_ind - target_ind), mode='nearest')
    return np.array([domain, values])
