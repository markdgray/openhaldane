from abc import ABCMeta, abstractmethod
import logging
import math
import sys

logging.basicConfig()

class Model(object):
    """ Decompression model abstract base class represents interface for dive compression models. """
    __metaclass__=ABCMeta

    @abstractmethod
    def update(self, P, t):
        pass

    @abstractmethod
    def ndl(self, t):
        pass

    @abstractmethod
    def reset(self, P, t):
        pass

    @staticmethod
    def factory(type):
        if type == "Buhlmann": return Buhlmann()
        assert 0, "Bad decompression model: " + type


class Buhlmann():
    """ Implementation of class Model using Buhlmann decompression model.

        References:
        * http://www.lizardland.co.uk/DIYDeco.html
        * http://njscuba.net/gear/trng_10_deco.php
        * http://wrobell.it-zone.org/decotengu/model.html

    """
    class Compartment():
        """ Class to represent a single compartment for the Buhlmann 
            decompression model.
        """
        
        water_pressure = 0.0567
        fN2 = 0.79
        atm = 1.013

        def __init__(self, halftime, a, b, logger):
            self.logger = logger
            self.k = math.log(2) / float(halftime)
            self.logger.debug("k calculated to be " + str(self.k) )
            self.halftime = halftime
            self.a = a
            self.b = b

        def reset(self, Pamb, current_time):
            self.Po = self.__alveolar_pressure(Pamb) # Initial compartment gas loading
            self.logger.debug("Initial pressure in compartment is " + str(self.Po) + " bar")
            self.Plast = Pamb
            self.last_time = current_time

        def update(self, Pamb, current_time):
            t = current_time - self.last_time
            self.Po = self.__schreiner_equation(Pio = self.__alveolar_pressure(Pamb), R = (Pamb - self.Plast) * self.fN2 / float(t), t = t, k= self.k, Po = self.Po)
            self.Plast = Pamb
            self.last_time = current_time
 
        def ascent_ceiling(self, t):
            Po = self.__schreiner_equation(Pio = self.__alveolar_pressure(self.Plast), R = 0, t = t, k = self.k, Po = self.Po)
            return self.__ascent_ceiling(Po)

        def __schreiner_equation(self, Pio, R, t, k, Po):
            return Pio + R * (t - 1/float(k)) - (Pio - Po - (R/float(k))) * math.exp(-1 * k * t) 
         
        def __alveolar_pressure(self, P):
            return (P - self.water_pressure) * self.fN2

        def __ascent_ceiling(self, Po):
            A = self.a
            B = self.b
            ascent_ceiling_bar = (Po - A) * B
            ascent_ceiling = (ascent_ceiling_bar - self.atm) * 10 #msw
            return ascent_ceiling

        def __convert_pressure_depth(self, pressure):
            return (pressure - self.atm) * 10 #msw             

           
    def __init__(self):
        self.logger = logging.getLogger('model(Buhlmann)')
        self.logger.setLevel(logging.DEBUG)
        self.compartments = list()
        self.compartments.append(self.Compartment(4,     1.2599, 0.5050, self.logger))
        self.compartments.append(self.Compartment(8,     1.0000, 0.6514, self.logger))
        self.compartments.append(self.Compartment(12.5,  0.8618, 0.7222, self.logger))
        self.compartments.append(self.Compartment(18.5,  0.7562, 0.7725, self.logger))
        self.compartments.append(self.Compartment(27,    0.6667, 0.8125, self.logger))
        self.compartments.append(self.Compartment(38.3,  0.5933, 0.8434, self.logger))
        self.compartments.append(self.Compartment(54.3,  0.5282, 0.8693, self.logger))
        self.compartments.append(self.Compartment(77,    0.4701, 0.8910, self.logger))
        self.compartments.append(self.Compartment(109,   0.4187, 0.9092, self.logger))
        self.compartments.append(self.Compartment(146,   0.3798, 0.9222, self.logger))
        self.compartments.append(self.Compartment(187,   0.3497, 0.9319, self.logger))
        self.compartments.append(self.Compartment(239,   0.3223, 0.9403, self.logger))
        self.compartments.append(self.Compartment(305,   0.2971, 0.9477, self.logger))
        self.compartments.append(self.Compartment(390,   0.2737, 0.9544, self.logger))
        self.compartments.append(self.Compartment(498,   0.2523, 0.9602, self.logger))
        self.compartments.append(self.Compartment(635,   0.2327, 0.9653, self.logger))

    def update(self, P, t):
         for compartment in self.compartments:
             compartment.update(P, t)
         
    def ndl(self):
         t = 0
         max_ceiling = 0
         while max_ceiling <= 0:
             max_ceiling = 0
             t = t + 1
             for compartment in self.compartments:
                 ceiling = compartment.ascent_ceiling(t)
                 if ceiling > max_ceiling:
                     max_ceiling = ceiling
             self.logger.debug("t(" + str(t) + "),max_ceiling(" + str(max_ceiling) + ")")

         # "t" requires decompression, so return prevous interval
         return t - 1

    def reset(self, P, t):
         for compartment in self.compartments:
             compartment.reset(P, t)

if __name__ == "__main__":
    d = 36
    P = 1.013/10 * d + 1.013
    print("Depth: ", d, ", P: ", P)
    print("Test Model")
    model = Model.factory("Buhlmann")
    model.reset(1.013, 0)
    model.update(P, 0.1)
    print("NDL: ", model.ndl())
    


