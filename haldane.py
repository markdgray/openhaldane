from sensor import *
from display import *
from timer import *
from model import *

import time

def main():
#    sensor = Sensor.factory("MS5803-14B")
    sensor = Sensor.factory("Dummy")
    model = Model.factory("Buhlmann")
    timer = Timer.factory("Dummy", 60)
    display = Display.factory("Stdio")

    ambient = 1.013
    print("- Starting Haldane -")
    
    model.reset(ambient, 0)
    

    while timer.wait():
        temp = sensor.getTemperature()
        pres = sensor.getPressure()  
        current_time =  timer.getTime()
        depth = (pres - ambient) * 10
        if depth < 0: depth = 0

        print(depth, pres,current_time)
        model.update(pres, current_time / 60 )
        ndl = model.ndl()
        if ndl == 99: ndl = "N/A"
        if ndl == 0: break

        display.display(ndl, current_time, depth, temp)
       

if __name__ == "__main__":
    main()
