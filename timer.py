from abc import ABCMeta, abstractmethod
import logging
import time

logging.basicConfig()

class Timer(object):
    """ Timer abstract base class represents interface for a periodic timer. """
    __metaclass__=ABCMeta

    @abstractmethod
    def wait(self):
        pass

    @staticmethod
    def factory(type, interval):
        if type == "Sleep": return Sleep(interval)
        assert 0, "Bad timer: " + type


class Sleep():
    """ Implementation of class Timer using a simple sleep command.

    """

    def __init__(self, interval):
        self.interval = interval 

    def wait(self):
        time.sleep(self.interval)


if __name__ == "__main__":
    print("Test Timer")
    timer = Timer.factory("Sleep", 1)
    for interval in range(0,9):
        timer.wait()
        print(time.strftime("%S"), " seconds")
