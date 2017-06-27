import unittest

from time import sleep

from ..timer import Timer


class TestTimer(unittest.TestCase):
    def test_initialization_default(self):
        # Given
        timer = Timer()

        # Then
        self.assertEqual(timer.elapsed, 0)

    def test_initialization_start(self):
        # Given
        timer = Timer(start=True)

        # Then
        self.assertGreater(timer.elapsed, 0)

    def test_stopwatch(self):
        # Given
        stopwatch = Timer()
        sleep_time = 0.00001

        # When
        stopwatch.start()
        sleep(sleep_time)
        stopwatch.stop()

        # Then
        self.assertGreater(stopwatch.elapsed, sleep_time)

    def test_context_manager(self):
        # Given
        sleep_time = 0.00001

        # When
        with Timer() as ctx_timer:
            sleep(sleep_time)

        # Then
        self.assertGreater(ctx_timer.elapsed, sleep_time)
