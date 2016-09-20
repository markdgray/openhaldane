from abc import ABCMeta, abstractmethod
import logging
import serial
import time

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
        if type == "Serial": return Serial()
        assert 0, "Bad display: " + type

class Serial():
    """ Implementation of class Display using serial port for
        an LCD-09393 (e.g. https://www.sparkfun.com/products/9393).

        Datasheet at https://www.sparkfun.com/datasheets/LCD/SerLCD_V2_5.PDF
 
        Prerequirsite for rpi: http://www.instructables.com/id/Read-and-write-from-serial-port-with-Raspberry-Pi/

    """
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyAMA0', 9600)
        time.sleep(0.5)
        self.__clear()
        self.__set_quad1() 
        self.serial.write(b"HALDANE")
        self.__set_quad3() 
        self.serial.write(b"Dive Computer")
        time.sleep(1)
        pass 

    def __clear(self):
        self.serial.write(b"\xFE\x01")

    # Set quadrant of the display
    def __set_quad1(self):
        self.serial.write(b"\xFE\x80")
    def __set_quad2(self):
        self.serial.write(b"\xFE\x87")
    def __set_quad3(self):
        self.serial.write(b"\xFE\xC0")
    def __set_quad4(self):
        self.serial.write(b"\xFE\xC7")

    def display(self, ndl, time, depth, temp):
        self.__clear() 
        self.__set_quad1() 
        text = 'N:' + str(ndl)
        self.serial.write(text.encode())
        self.__set_quad3() 
        text = 'D:' + "{:.1f}".format(depth)
        self.serial.write(text.encode())
        self.__set_quad2() 
        text = 't:' + str(time)
        self.serial.write(text.encode())
        self.__set_quad4() 
        text = 'T:' + "{:.1f}".format(temp)
        self.serial.write(text.encode())

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
    display = Display.factory("Serial")
    display.display(10,1,10,273)
