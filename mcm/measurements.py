import logging
from math import ceil
import numpy as np
from scipy.ndimage import shift

__all__ = ["calculate_number_of_peaks", "sum_peak_to_one", "check_conditions_with_weights", "roll_peak_to_val"]


def calculate_peak_width(peak):
    maximum = peak[1].max()
    value = 0.8 * maximum

    left_ind = where_is_this_val(value, peak[1], left=True)
    right_ind = where_is_this_val(value, peak[1], left=False)

    return right_ind - left_ind


def calculate_number_of_peaks(begin, end, peak):
    width_in_ind = calculate_peak_width(peak)
    begin_ind = where_is_this_val(begin, peak[0])
    end_ind = where_is_this_val(end, peak[0])

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


def where_is_this_val(val, one_dim_array, left=True):
    """Return just one, the most left or right index of given value"""
    if left:
        return (np.abs(one_dim_array - val)).argmin()
    else:
        return (np.abs(one_dim_array - val)).argmax()


def check_conditions_old(begin, end, sum_peak):
    domain = sum_peak[0]
    values = sum_peak[1]
    ind_begin = where_is_this_val(begin, domain)
    ind_end = where_is_this_val(end, domain)

    interesting_part = values[ind_begin:ind_end]
    return np.abs(1 - np.mean(interesting_part))


def check_conditions_with_weights(begin, end, sum_peak):
    """We want to minimize this result (get closest to 0)

    Score weights (sector = [begin; end]):
        Pre sector weight: 0.35
        Sector score weight: 0.5
        Post sector weight: 0.15
    """
    domain = sum_peak[0]
    values = sum_peak[1]
    ind_begin = where_is_this_val(begin, domain)
    ind_end = where_is_this_val(end, domain)

    pre_penalty = np.abs(values[0:ind_begin].sum())
    post_penalty = np.abs(values[ind_end:-1].sum())

    middle_sector = np.array(values[ind_begin:ind_end]) - 1
    middle_penalty = np.abs(middle_sector.sum())

    return (pre_penalty * 0.35) + (middle_penalty * 0.5) + (post_penalty * 0.15)


def roll_peak_to_val(peak, target_val):
    domain = peak[0]
    values = peak[1]
    target_ind = (np.abs(domain - target_val)).argmin()
    max_peak_val_ind = np.argmax(values)
    logging.debug("Target shift index = %s\nMax peak value index = %s" % (target_ind, max_peak_val_ind))
    values = shift(values, -(max_peak_val_ind - target_ind), mode='nearest')
    return np.array([domain, values])
