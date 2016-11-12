import threading
from time import strftime, localtime, time, sleep

import math


def get_location_string(location):
    if location[0] is None or location[1] is None:
        return "N/A"
    else:
        if location[0] >= 0:
            lat_string = '{0:.3f}° N'.format(location[0])
        else:
            lat_string = '{0:.3f}° S'.format(location[0])

        if location[1] >= 0:
            lon_string = '{0:.3f}° E'.format(location[1])
        else:
            lon_string = '{0:.3f}° W'.format(location[1])

        return '{0} {1}'.format(lat_string, lon_string)


def format_speed(speed):
    if speed is None:
        return "N/A"
    else:
        return '{:.1f} km/h'.format(speed * 3.6)


def format_time(time):
    if time is not None:
        return strftime("%d-%m-%Y %H:%M:%S", localtime(time))
    else:
        return "N/A"


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    '''
    Python 2 implementation of Python 3.5 math.isclose()
    https://hg.python.org/cpython/file/tip/Modules/mathmodule.c#l1993
    '''
    # sanity check on the inputs
    if rel_tol < 0 or abs_tol < 0:
        raise ValueError("tolerances must be non-negative")

    # short circuit exact equality -- needed to catch two infinities of
    # the same sign. And perhaps speeds things up a bit sometimes.
    if a == b:
        return True

    # This catches the case of two infinities of opposite sign, or
    # one infinity and one finite number. Two infinities of opposite
    # sign would otherwise have an infinite relative tolerance.
    # Two infinities of the same sign are caught by the equality check
    # above.
    if math.isinf(a) or math.isinf(b):
        return False

    # now do the regular computation
    # this is essentially the "weak" test from the Boost library
    diff = math.fabs(b - a)
    result = (((diff <= math.fabs(rel_tol * b)) or
               (diff <= math.fabs(rel_tol * a))) or
              (diff <= abs_tol))
    return result


class IntervalTimer(threading.Thread):
    def __init__(self, interval_in_seconds, function):
        super().__init__()
        self._isStopped = threading.Event()
        self._interval_in_seconds = interval_in_seconds
        self._timer_function = function

    def run(self):
        while not self._isStopped.is_set():
            sleep(self._interval_in_seconds)
            self._timer_function()

        self._isStopped.clear()

    def stop(self):
        self._isStopped.set()

