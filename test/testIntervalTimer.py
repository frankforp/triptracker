from unittest import TestCase

import time

from utils.IntervalTimer import IntervalTimer


class IntervalTimerTest(TestCase):
    def setUp(self):
        self.counter = 0

    def testIntervalTimer_with4SecondsInterval_shouldExecuteTwiceIn8Seconds(self):
        timer = IntervalTimer(4, self.timer_function)
        timer.start()
        time.sleep(8)
        timer.stop()
        self.assertEqual(2, self.counter)

    def timer_function(self):
        self.counter += 1
