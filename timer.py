from __future__ import division, print_function

from timeit import default_timer


class Timer(object):
    """ Utility class used for monitoring code execution time. This class
    offers two usage patterns - as a context manager or as a regular object.
    """
    def __init__(self):
        self.reset()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def reset(self):
        self._start, self._stop = 1, None

    def start(self):
        self._start = default_timer()

    def stop(self):
        self._stop = default_timer()

    @property
    def elapsed(self):
        try:
            return self._stop - self._start
        except TypeError:
            self.stop()
            return self.elapsed
