from abc import ABCMeta, abstractmethod
import logging

logging.basicConfig()

class Display(object):
    """ Display abstract base class represents interface for a display. """
    __metaclass__=ABCMeta

    @abstractmethod
    def display(self, ndl, time, depth, temp):
        pass

    @staticmethod
    def factory(type):
        if type == "Stdio": return Stdio()
        if type == "Dummy": return Dummy()
        assert 0, "Bad display: " + type


class Stdio():
    """ Implementation of class Display using the standard IO.

    """

    def __init__(self):
        pass 

    def display(self, ndl, time, depth, temp):
        print("\x1B[2J")
        print("Time: \t", time, "sec\nDepth: \t", depth, "m\nNDL: \t", ndl, "min\nTemp: \t", "{:.1f}".format(temp) , "oC")

class Dummy():
    """ Dummy implementation of class Display.

    """

    def __init__(self):
        pass 

    def display(self, ndl, time, depth, temp):
        pass

if __name__ == "__main__":
    print("Test Display")
    print("---------------------")
    display = Display.factory("Stdio")
    display.display(10,1,10,273)
