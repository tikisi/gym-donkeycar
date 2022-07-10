import time


class FPSTimer(object):
    """
    Every N on_frame events, give the average iterations per interval.
    """

    def __init__(self, name='', N=100):
        self.t = time.perf_counter()
        self.iter = 0
        self.N = N
        self.name = name

    def reset(self):
        self.t = time.perf_counter()
        self.iter = 0

    def on_frame(self):
        self.iter += 1
        if self.iter == self.N:
            e = time.perf_counter()
            print(f'[fps]{self.name}: ', float(self.N) / (e - self.t))
            self.t = time.perf_counter()
            self.iter = 0
