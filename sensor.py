from abc import ABCMeta, abstractmethod
from quick2wire import i2c
import logging
import time

logging.basicConfig()

class Sensor(object):
    """ Sensor abstract base class represents interface for pressure sensors. """
    __metaclass__=ABCMeta

    @abstractmethod
    def getPressure(self):
        pass

    @abstractmethod
    def getTemperature(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @staticmethod
    def factory(type):
        if type == "MS5803-14B": return MS5803()
        assert 0, "Bad sensor type: " + type


class MS5803():
    """ Implementation of class Sensor for the Amsys MS5803-14BA pressure sensor.

        Implementation of abstract base class Sensor for the Amsys MS5803-14BA 
        pressure sensor has been derived from sensor datasheet at 
        http://www.amsys-sensor.eu/sheets/amsys.en.ms5803_14ba.pdf.

    """
    def __init__(self):
        self.logger = logging.getLogger('sensor(MS5803)')
        self.logger.setLevel(logging.DEBUG)
        self.bus = i2c.I2CMaster(1)
        self.address = 0x77
        self.C = [0 for i in range(7)]
        self.D = [0 for i in range(3)]
        for x in range(1,7):
            self.C[x] = self.__readPROM(x) 

    def reset(self):
        self.bus.transaction(i2c.writing_bytes(self.address, 0x1E))
        time.sleep(0.01)

    def __readPROM(self, address):
        #PROM read code
        command = 0xA0 + (address << 1)
        values = self.bus.transaction(i2c.writing_bytes(self.address, command), i2c.reading(self.address, 2))
        C = (values[0][0] << 8) | values[0][1]
        self.logger.debug("CMD(" + "{0:#04x}".format(command) + ") -> " + "C = " + str(C))
        return C

    def __readADC(self):
        command = 0x00
        #Read D1
        self.bus.transaction(i2c.writing_bytes(self.address, 0x48))
        time.sleep(0.01)
        values = self.bus.transaction(i2c.writing_bytes(self.address, command), i2c.reading(self.address, 3))
        self.D[1] = (values[0][0] << 16) | (values[0][1] << 8) | (values[0][2])
        self.logger.debug("CMD(" + "{0:#04x}".format(command) + ") -> D1 = " + str(self.D[1])) 
        # Read D2
        self.bus.transaction(i2c.writing_bytes(self.address, 0x58))
        time.sleep(0.01)
        values = self.bus.transaction(i2c.writing_bytes(self.address, command), i2c.reading(self.address, 3))
        self.D[2] = (values[0][0] << 16) | (values[0][1] << 8) | (values[0][2])
        self.logger.debug("CMD(" + "{0:#04x}".format(command) + ") -> D2 = " + str(self.D[2])) 

    def __calc(self):
        self.__readADC()
        dT = self.D[2] - self.C[5] * 256
        TEMP = 2000 + dT * self.C[6] / 8388608
        OFF = self.C[2] * 65536 + (self.C[4] * dT) / 128
        SENS = self.C[1] * 32768 + (self.C[3] * dT) / 256
        P = (self.D[1] * SENS / 2097152 - OFF) / 32768
        return (TEMP, P)

    def getTemperature(self):
        return self.__calc()[0]      

    def getPressure(self):
        return self.__calc()[1]




if __name__ == "__main__":
    print("Getting sensor values:")
    sensor = Sensor.factory("MS5803-14B")
    sensor.reset()
    temp = sensor.getTemperature() / 100.0
    print("Temperature is ", str(temp), " deg celsius")
    pressure = sensor.getPressure() / 10.0
    print("Pressure is ", str(pressure), " mbar")
    
