from random import uniform, choice


def random_peaks_with_positions(begin, end, peaks, n):
    """
    Return n pairs (random peak from peaks, random number from <begin, end>)
    :param begin:
    :param end:
    :param peaks: this should be a list
    :return: list of pairs (peak, position)
    """
    return [(choice(peaks), uniform(begin, end)) for _ in range(n)]


def random_positions(peaks):
    return [uniform(0, 40) for _ in range(len(peaks))]
