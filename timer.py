from abc import ABCMeta, abstractmethod
import logging
import time
import pause

logging.basicConfig()

class Timer(object):
    """ Timer abstract base class represents interface for a periodic timer. """
    __metaclass__=ABCMeta

    @abstractmethod
    def wait(self):
        pass
     
    @abstractmethod
    def getTime(self):
        pass

    @staticmethod
    def factory(type, interval):
        if type == "Sleep": return Sleep(interval)
        if type == "Dummy": return Dummy(interval)
        assert 0, "Bad timer: " + type


class Sleep():
    """ Implementation of class Timer using a simple sleep command.

    """
    def __init__(self, interval):
        self.interval = interval 
        self.last = int(time.time())
        self.start = self.last

    def wait(self):
        pause.until(self.last + self.interval)
        self.last = self.last + self.interval
        return True

    def getTime(self):
        return int(time.time()) - self.start

class Dummy():
    """ Dummy implementation of class Timer for testing.

    """
    def __init__(self, interval):
        self.interval = interval 
        self.time = 0

    def wait(self):
        self.time = self.time + self.interval
        return True

    def getTime(self):
        return self.time

if __name__ == "__main__":
    print("Test Timer")
    timer = Timer.factory("Sleep", 1)
    for interval in range(0,9):
        timer.wait()
        print(timer.getTime(), " seconds")
