from __future__ import division, print_function

from timeit import default_timer


class Timer(object):
    """ Utility class used for monitoring code execution time. This class
    offers two usage patterns - as a context manager or as a regular object.
    """
    def __init__(self, start=False):
        """ Initialize the Timer and optionally start it.

        Parameters
        ----------
        start : bool
            Flag indicating whether to start the timer.
        """
        self.reset(start=start)

    def __enter__(self):
        self.reset(start=True)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def reset(self, start=False):
        """ Reset the Timer and the optionally start it.

        Parameters
        ----------
        start : bool
            Flag indicating whether to start the timer.
        """
        self._start, self._stop = 0, 0
        self._stopped = True
        if start:
            self.start()

    def start(self):
        """ Start the Timer."""
        self._start = default_timer()
        self._stopped = False

    def stop(self):
        """ Stop the Timer."""
        self._stop = default_timer()
        self._stopped = True

    @property
    def elapsed(self):
        """ Property for getting the elapsed time. Stops the Timer if it has
        not been stopped explicitly.
        """
        if not self._stopped:
            self.stop()
            return self.elapsed
        return self._stop - self._start
