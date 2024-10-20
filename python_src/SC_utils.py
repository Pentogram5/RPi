import time

class TimeStamper:
    def __init__(self):
        self.old_t = time.time()

    def timestamp(self):
        dt = time.time() - self.old_t
        self.old_t = time.time()
        return dt

class ThreadRate:
    """Утилита для сна с фиксированной частотой."""

    def __init__(self, freq=1):
        self.freq = freq
        self._period = 1 / self.freq
        self.ts = TimeStamper()

    def sleep(self):
        # print(self._period - self.ts.timestamp())
        sleep_time = max(self._period - self.ts.timestamp(), 0)
        time.sleep(sleep_time)
        return sleep_time

    def get_sleep_time(self):
        return max(self._period - self.ts.timestamp(), 0)