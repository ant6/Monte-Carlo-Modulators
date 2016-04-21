from math import ceil
import logging

from mcm.peak_reader import transposed


def calculate_peak_width(peak):
    # calculate maximum value
    values = transposed(peak)[1]
    maximum = max(values)
    value = 0.8 * maximum

    # first we go from the left
    left_x = x_at_given_y(peak, value, search_from_end=False)

    # now from the right
    right_x = x_at_given_y(peak, value, search_from_end=True)

    return right_x - left_x


def x_at_given_y(input_data, y_value, search_from_end=False, interpolate=True):
    # sort comparing [0]th element from each pair
    input_data_sorted_by_x = sorted(input_data, key=lambda pair: pair[0])

    if search_from_end:
        input_data_sorted_by_x.reverse()

    if input_data_sorted_by_x[0][1] > y_value:
        return input_data_sorted_by_x[0][0]

    x_value = float('nan')
    for i in range(len(input_data_sorted_by_x) - 1):
        xcur, ycur = input_data_sorted_by_x[i]
        xnext, ynext = input_data_sorted_by_x[i + 1]
        if ynext == ycur and y_value == ycur:
            x_value = xcur
            break
        if min(ycur, ynext) <= y_value <= max(ycur, ynext):
            if interpolate:
                x_value = xcur + ((xnext - xcur) / float(ynext - ycur)) * (y_value - ycur)
            else:
                x_value = xcur
            break

    return float(x_value)


def calculate_number_of_peaks(begin, end, peak):
    # calculate BP's width at 80%
    width = calculate_peak_width(peak)

    # we take ceiling of the result
    number_of_peaks = 1 + int(ceil((end - begin) / width))

    position_step = (begin - end) / number_of_peaks
    positions = []
    for n in range(number_of_peaks):
        positions.append(end - n * position_step)
    positions.append(begin)

    logging.debug("Position step = %s\nSorted positions = %s" % (position_step, sorted(positions)))
    # return sorted values
    return sorted(positions)
