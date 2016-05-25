from sensor import *
from display import *
from timer import *
from model import *

import time

def main():
    sensor = Sensor.factory("MS5803-14B")
    model = Model.factory("Buhlmann")
    timer = Timer.factory("Sleep", 1)
    display = Display.factory("Stdio")

    print("- Starting Haldane -")
    temp = sensor.getTemperature()
    pres = sensor.getPressure()  
    
    start_time = int(time.time())
    model.reset(pres, 0)
    

    while timer.wait():
        temp = sensor.getTemperature()
        pres = sensor.getPressure()  
        current_time = int(time.time()) - start_time
        print(current_time)
        depth = (pres - 1.013) * 10
        if depth < 0: depth = 0

        model.update(pres, current_time)
        ndl = model.ndl()
        if ndl == 99: ndl = "N/A"

        display.display(ndl, current_time, depth, temp)

       

if __name__ == "__main__":
    main()
