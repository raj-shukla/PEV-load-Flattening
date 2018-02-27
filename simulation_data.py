from csv import reader
from math import exp
from operator import itemgetter
import random



def SimulationData():
    vehicles = 100
    schedules = 300
    scheduleTime = 1/12
    initialTime = 7
    voltageOne = 2
    voltageTwo = 4
    voltageThree = 6
    arrivalTime = []
    departureTime = []
    SOCr = []
    currentOne = []
    currentTwo = []
    currentThree = []
   
    for i in range(0, 1000) :
    #{
        arrivalTime.append(random.randrange(7, 17))
        departureTime.append(arrivalTime[i] + random.randrange(1, 10))
        SOCr.append(random.randrange(15, 50))
        currentOne.append(random.randrange(1, 3))
        currentTwo.append(random.randrange(4, 7))
        currentThree.append(random.randrange(8, 11))
    #}


        
    return [vehicles, schedules, scheduleTime, initialTime,  voltageOne, voltageTwo, voltageThree, SOCr, arrivalTime, departureTime, currentOne, currentTwo, currentThree]
#}

SimulationData()

