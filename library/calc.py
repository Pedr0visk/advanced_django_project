import math


def exponential(failure_rate, time):
    """
    This function returns the complement of a test for each
    for test in tests:
        sub = 1 - (1 - math.exp((-1) * test.interval * step * (dt) * test.coverage))
        pols.append(sub)
    # pols = [0.234523, 0.53244, 0.12345]
    return 1 - reduce(lambda x, y: x*y), pols)
    """
    return 1 - math.exp((-1) * float(failure_rate) * time)


def probability(probability, time):
    return 1 - (float(probability) * time)


def weibull(coverage, scale, form, time):
    return 1 - math.exp(((-1) * float(coverage) * float(scale) * float(form) * time))


def step():
    return 1
