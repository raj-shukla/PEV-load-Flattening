import math
import csv
from operator import itemgetter
import random
import statistics
import copy
import time
import simulation_data




def Simulation (simulationData) :
#{
    vehicles = simulationData[0]
    schedules = simulationData[1]
    scheduleTime = simulationData[2]
    initialTime = simulationData[3]
    voltageOne = simulationData[4]
    voltageTwo = simulationData[5]
    voltageThree = simulationData[6]
    SOCr = simulationData[7][:vehicles]
    arrivalTime = simulationData[8][:vehicles]
    departureTime = simulationData[9][:vehicles]
    currentOne = simulationData[10][:vehicles]
    currentTwo = simulationData[11][:vehicles]
    currentThree = simulationData[12][:vehicles]
    powerToCharge = []
    timeToCharge = []
    timeToChargeRatio = []
    aSchedule = []
    for i in range(0, vehicles):
    #{
        powerToCharge.append(voltageTwo*currentTwo[i])
        timeToCharge.append(SOCr[i]/powerToCharge[i])
        if((departureTime[i] - arrivalTime[i]) < timeToCharge[i]) :
        #{
            timeToCharge[i] = 0.75 * (departureTime[i] - arrivalTime[i])
        #}
        timeToChargeRatio.append(timeToCharge[i]/(departureTime[i] - arrivalTime[i]))
        aSchedule.append([])
    #}
    netPower = []
    for i in range (0, schedules) :
    #{
        netPower.append(0)
    #}

        
    tmpList = []
    sortedList = []
    tmpList = zip(SOCr, arrivalTime, departureTime, currentOne, currentTwo, currentThree, powerToCharge, timeToCharge, timeToChargeRatio)
    sortedList = sorted(tmpList, key = itemgetter(1))

    
    def FindMinPowerSlots(vehicleList) :
    #{
        arrivalSlot = math.ceil((vehicleList[1] - initialTime)/scheduleTime)
        departureSlot = math.floor((vehicleList[2] - initialTime)/scheduleTime)
        slotsToCharge = math.ceil(vehicleList[7]/scheduleTime)
        windowLength = 0
        windowIncrement = 5
        assigned = False
        startWindow = min(netPower[arrivalSlot:departureSlot + 1])
        startIndex = arrivalSlot
        endIndex =  departureSlot - slotsToCharge + 1
        while(assigned is not True) :
        #{
            windowLength = windowLength + windowIncrement
            for i in range(startIndex, endIndex + 1):
            #{
                if all( startWindow <= j < startWindow + windowLength for j in netPower[i:i + slotsToCharge]) :
                #{
                    netPower[i: i + slotsToCharge ] = list(map(lambda x: x + voltageTwo * vehicleList[4], netPower[i:i + slotsToCharge]  ))
                    assigned = True
                    return[vehicleList, i, slotsToCharge, voltageTwo*vehicleList[4], 2]
                #}
            #}
        #}
    #}
    for i in range(0, len(sortedList)):
    #{
        aSchedule[i] = FindMinPowerSlots(sortedList[i])
        vehicleCount = i + 1
    #}
        

    aSchedule.sort(key = itemgetter(1))
    
    def FindValues(nPower) :
    #{
        deltaP = 0
        count = 0
        aPowerV = nPower[:]
        while(nPower[-1] == 0):
        #{
            nPower.pop(-1)
        #}
        for i in range(0, len(nPower)-1):
        #{
            if(nPower[i] != nPower[i+1]):
            #{
                count = count + 1
            #}
            deltaP = deltaP + abs(nPower[i] - nPower[i+1])
        #}
        deltaPavg = deltaP/len(nPower)
        deltaPvariation = deltaP/count
        pFactor = max(nPower)/statistics.mean(nPower)
        return [aPowerV, deltaP, deltaPavg, count, deltaPvariation, pFactor]
    #}
    parameters = FindValues(netPower[:])
    Alist = parameters[:] 
    assignedPower = netPower[:]
    avgPowerMin = min(netPower)
    avgPowerMax = max(netPower)
    averagePower = avgPowerMin
   
    
    while(averagePower < avgPowerMax):
    #{
        averagePower = averagePower + 1
        lIndexList = [[], []]
        hIndexList = [[], []]
        lStartIndex = 0
        lEndIndex = 0
        hStartIndex = 0
        hEndIndex = 0
        for i, val in enumerate(netPower):
        #{
            if (netPower[i] <=averagePower):
            #{
                if (lStartIndex == lEndIndex):
                #{
                    lIndexList[0].append(i)
                #}
                lEndIndex = lEndIndex + 1
                if (i == len(netPower) - 1):
                #{
                    lIndexList[1].append(i)
                #}

                if (hStartIndex != hEndIndex):
                #{
                    hIndexList[1].append(i -1)
                #}
                hStartIndex = i
                hEndIndex = i

            #}
            if (netPower[i] > averagePower):
            #{
                if (hStartIndex == hEndIndex):
                #{
                    hIndexList[0].append(i)
                #}
                hEndIndex = hEndIndex + 1
                if (i == len(netPower) - 1):
                #{
                    hIndexList[1].append(i)
                #}
                if (lStartIndex != lEndIndex):
                #{
                    lIndexList[1].append(i -1)
                #}
                lStartIndex = i
                lEndIndex = i
            #}
        #}
       
 
        for i in range(0, len(lIndexList[0])):
        #{
            for j in range(0, len(aSchedule)):
            #{
                if(lIndexList[0][i] <= aSchedule[j][1] and lIndexList[1][i] >=aSchedule[j][1] + aSchedule[j][2] and all ( j < averagePower and j>0 for  j in netPower[aSchedule[j][1]: aSchedule[j][1] + aSchedule[j][2]]) ):
                #{
                    if(aSchedule[j][4] == 2):
                    #{
                        nSlot = math.ceil((aSchedule[j][0][0]/(voltageThree*aSchedule[j][0][5]))/scheduleTime)
                        sSlot = aSchedule[j][1]
                        eSlot = aSchedule[j][1] + nSlot
                        pReduce = aSchedule[j][3]
                        pIncrease = voltageThree*aSchedule[j][0][5]
                        if (all (0 < j - pReduce  + pIncrease < averagePower for j in netPower[sSlot:eSlot])):
                        #{
                            netPower[sSlot:aSchedule[j][1] + aSchedule[j][2]] = list(map(lambda x: x - pReduce, netPower[sSlot:aSchedule[j][1] + aSchedule[j][2]]  ))
                            netPower[sSlot:eSlot] = list(map(lambda x: x + pIncrease, netPower[sSlot:eSlot]))
                            aSchedule[j][2] = nSlot
                            aSchedule[j][4] =  3
                    #}
                    #}
                #}
            #}
        
        
        for i in range(0, len(hIndexList[0])):
        #{
            for j in range(0, len(aSchedule)):
            #{
                if(aSchedule[j][4] == 2):
                #{
                    if(hIndexList[0][i] <= aSchedule[j][1] and hIndexList[1][i] >=aSchedule[j][1] + aSchedule[j][2] and all ( j > averagePower and j > 0 for  j in netPower[aSchedule[j][1]: aSchedule[j][1] + aSchedule[j][2]]) ):
                    #{
                        nSlot = math.ceil((aSchedule[j][0][0]/(voltageOne*aSchedule[j][0][3]))/scheduleTime)
                        sSlot = aSchedule[j][1]
                        eSlot = aSchedule[j][1] + nSlot
                        dSlot = math.floor((aSchedule[j][0][2] - initialTime)/scheduleTime)
                        pReduce = aSchedule[j][3]
                        pIncrease = voltageOne*aSchedule[j][0][3]
                        if (dSlot >= eSlot-1  and  all (0 <= j - pReduce  + pIncrease >  averagePower for j in netPower[sSlot:eSlot])):
                        #{
                            netPower[sSlot:aSchedule[j][1] + aSchedule[j][2]] = list(map(lambda x: x - pReduce, netPower[sSlot:aSchedule[j][1] + aSchedule[j][2]]  ))
                            netPower[sSlot:eSlot] = list(map(lambda x: x + pIncrease, netPower[sSlot:eSlot]))
                            aSchedule[j][2] = nSlot
                            aSchedule[j][4] =  1
                    #}
                #}
                #}
            #}
        #}
        lIndexList.clear()
        lIndexList = [[], []]
        lStartIndex = 0
        lEndIndex = 0
        
        
        for i, val in enumerate(netPower):
        #{
            if (netPower[i] <=averagePower):
            #{
                if (lStartIndex == lEndIndex):
                #{
                    lIndexList[0].append(i)
                #}
                lEndIndex = lEndIndex + 1
                if (i == len(netPower) - 1):
                #{
                    lIndexList[1].append(i)
                #}
            #}
            if (netPower[i] > averagePower):
            #{
                if (lStartIndex != lEndIndex):
                #{
                    lIndexList[1].append(i -1)
                #}
                lStartIndex = i
                lEndIndex = i
            #}
        #}

       
        
        for i in range(0,len(lIndexList[0])):
        #{
            for j in range(0, len(aSchedule)):
            #{
                dSlot = math.floor((aSchedule[j][0][2] - initialTime)/scheduleTime)
                sSlot = aSchedule[j][1]
                nSlot = aSchedule[j][2]
                if(lIndexList[0][i] <= sSlot + nSlot and lIndexList[1][i] >=dSlot and all ( j > averagePower for  j in netPower[sSlot: sSlot + nSlot] )):
                #{
                   if(aSchedule[j][4] == 1):
                   #{
                       aPower = voltageOne*aSchedule[j][0][3]
                   #}
                   if(aSchedule[j][4] == 2):
                   #{
                       aPower = voltageTwo*aSchedule[j][0][4]
                   #}
                   if(aSchedule[j][4] == 3):
                   #{
                       aPower = voltageOne*aSchedule[j][0][5]
                   #}
                   netPower[sSlot:sSlot + nSlot] = list(map(lambda x: x - aPower, netPower[sSlot:sSlot + nSlot]  ))
                   netPower[dSlot - nSlot + 1:dSlot + 1] = list(map(lambda x: x + aPower, netPower[dSlot - nSlot + 1:dSlot + 1]))
                   aSchedule[j][1] = dSlot - nSlot + 1
                #}
            #}
        #}

        
        parameters = FindValues(netPower[:])
        if(parameters[5] <= Alist[5]):
        #{
            Alist = parameters[:]
        #}
        
    #}
    return (Alist)
#}


def SimulationArrivalFirst(simulationData):
#{
    vehicles = simulationData[0]
    schedules = simulationData[1]
    scheduleTime = simulationData[2]
    initialTime = simulationData[3]
    voltageOne = simulationData[4]
    voltageTwo = simulationData[5]
    voltageThree = simulationData[6]
    SOCr = simulationData[7][:vehicles]
    arrivalTime = simulationData[8][:vehicles]
    departureTime = simulationData[9][:vehicles]
    currentOne = simulationData[10][:vehicles]
    currentTwo = simulationData[11][:vehicles]
    currentThree = simulationData[12][:vehicles]
    powerToCharge = []
    timeToCharge = []
    timeToChargeRatio = []
    aSchedule = []
    for i in range(0, vehicles):
    #{
        powerToCharge.append(voltageTwo*currentTwo[i])
        timeToCharge.append(SOCr[i]/powerToCharge[i])
        if((departureTime[i] - arrivalTime[i]) < timeToCharge[i]) :
        #{
            timeToCharge[i] = 0.75 * (departureTime[i] - arrivalTime[i])
        #}
        timeToChargeRatio.append(timeToCharge[i]/(departureTime[i] - arrivalTime[i]))
        aSchedule.append([])
    #}
    netPower = []
    for i in range (0, schedules) :
    #{
        netPower.append(0)
    #}
    tmpList = []
    sortedList = []
    tmpList = zip(SOCr, arrivalTime, departureTime, currentOne, currentTwo, currentThree, powerToCharge, timeToCharge, timeToChargeRatio)
    sortedList = sorted(tmpList, key = itemgetter(1))

    def FindSlots(vehicleList):
    #{
        arrivalSlot = math.ceil((vehicleList[1] - initialTime)/scheduleTime)
        departureSlot = math.floor((vehicleList[2] - initialTime)/scheduleTime)
        slotsToCharge = math.ceil(vehicleList[7]/scheduleTime)
        netPower[arrivalSlot:arrivalSlot + slotsToCharge] = list(map(lambda x: x + voltageTwo * vehicleList[4], netPower[arrivalSlot:arrivalSlot + slotsToCharge]))
    #}
    
    for i in range(0, len(sortedList)):
    #{
        FindSlots(sortedList[i])
    #}

    def FindValues(nPower) :
    #{
        deltaP = 0
        count = 0
        aPowerV = nPower[:]
        while(nPower[-1] == 0):
        #{
            nPower.pop(-1)
        #}
        for i in range(0, len(nPower)-1):
        #{
            if(nPower[i] != nPower[i+1]):
            #{
                count = count + 1
            #}
            deltaP = deltaP + abs(nPower[i] - nPower[i+1])
        #}
        deltaPavg = deltaP/len(nPower)
        deltaPvariation = deltaP/count
        pFactor = max(nPower)/statistics.mean(nPower)
        return [aPowerV, deltaP, deltaPavg, count, deltaPvariation, pFactor]
    #}
    parameters = FindValues(netPower[:])
    return parameters
#}

def SimulationRandom(simulationData):
#{
    vehicles = simulationData[0]
    schedules = simulationData[1]
    scheduleTime = simulationData[2]
    initialTime = simulationData[3]
    voltageOne = simulationData[4]
    voltageTwo = simulationData[5]
    voltageThree = simulationData[6]
    SOCr = simulationData[7][:vehicles]
    arrivalTime = simulationData[8][:vehicles]
    departureTime = simulationData[9][:vehicles]
    currentOne = simulationData[10][:vehicles]
    currentTwo = simulationData[11][:vehicles]
    currentThree = simulationData[12][:vehicles]
    powerToCharge = []
    timeToCharge = []
    timeToChargeRatio = []
    aSchedule = []
    for i in range(0, vehicles):
    #{
        powerToCharge.append(voltageTwo*currentTwo[i])
        timeToCharge.append(SOCr[i]/powerToCharge[i])
        if((departureTime[i] - arrivalTime[i]) < timeToCharge[i]) :
        #{
            timeToCharge[i] = 0.75 * (departureTime[i] - arrivalTime[i])
        #}
        timeToChargeRatio.append(timeToCharge[i]/(departureTime[i] - arrivalTime[i]))
        aSchedule.append([])
    #}
    netPower = []
    for i in range (0, schedules) :
    #{
        netPower.append(0)
    #}
    tmpList = []
    sortedList = []
    tmpList = zip(SOCr, arrivalTime, departureTime, currentOne, currentTwo, currentThree, powerToCharge, timeToCharge, timeToChargeRatio)
    sortedList = sorted(tmpList, key = itemgetter(1))

    def FindSlots(vehicleList):
    #{
        arrivalSlot = math.ceil((vehicleList[1] - initialTime)/scheduleTime)
        departureSlot = math.floor((vehicleList[2] - initialTime)/scheduleTime)
        slotsToCharge = math.ceil(vehicleList[7]/scheduleTime)
        randSlot = random.randrange(arrivalSlot, departureSlot - slotsToCharge + 2)
        
        netPower[randSlot:randSlot + slotsToCharge] = list(map(lambda x: x + voltageTwo * vehicleList[4], netPower[randSlot:randSlot + slotsToCharge]))
    #}
    
    for i in range(0, len(sortedList)):
    #{
        FindSlots(sortedList[i])
    #}

    def FindValues(nPower) :
    #{
        deltaP = 0
        count = 0
        aPowerV = nPower[:]
        while(nPower[-1] == 0):
        #{
            nPower.pop(-1)
        #}
        for i in range(0, len(nPower)-1):
        #{
            if(nPower[i] != nPower[i+1]):
            #{
                count = count + 1
            #}
            deltaP = deltaP + abs(nPower[i] - nPower[i+1])
        #}
        deltaPavg = deltaP/len(nPower)
        deltaPvariation = deltaP/count
        pFactor = max(nPower)/statistics.mean(nPower)
        return [aPowerV, deltaP, deltaPavg, count, deltaPvariation, pFactor]
    #}
    parameters = FindValues(netPower[:])
    return parameters
#}

listSimulation = []
listAfirst = []
listRandom = []
aSlotSimulationMean = []
aParametersSimulationMean = []
aSlotArrivalFirstMean = []
parametersArrivalFirstMean = []
aSlotRandomMean = []
parametersRandomMean = []
executionTime = []
executionTimeMean = []
variable = []

variableParameter = 0
for i in range(0, 10):
#{
    variableParameter = variableParameter + 50
    variable.append(variableParameter)
    for i in range(0, 100):
    #{
        simulationData = simulation_data.SimulationData()
        simulationData[0] = variableParameter
        startTime = time.time()
        listSimulation.append(Simulation(simulationData))
        endTime = time.time()
        executionTime.append(endTime - startTime)
        #listAfirst.append(SimulationArrivalFirst(simulationData))
        #listRandom.append(SimulationRandom(simulationData)) 
    #}
    print(executionTime)
    executionTimeMean.append(statistics.mean(executionTime))
    executionTime.clear()
    '''
    aSlotLsimulation = [i[0] for i in listSimulation]
    parameterLsimulation = [i[1:] for i in listSimulation]
    aSlotSimulationMean.append(list(map(statistics.mean, zip(*aSlotLsimulation))))
    aParametersSimulationMean.append(list(map (statistics.mean, zip(*parameterLsimulation))))
    aSlotLarrivalFirst = [i[0] for i in listAfirst]
    parameterLarrivalFirst = [i[1:] for i in listAfirst]
    aSlotArrivalFirstMean.append(list(map(statistics.mean, zip(*aSlotLarrivalFirst))))
    parametersArrivalFirstMean.append(list(map(statistics.mean, zip(*parameterLarrivalFirst))))
    aSlotLrandom = [i[0] for i in listRandom]
    parameterLrandom = [i[1:] for i in listRandom]
    aSlotRandomMean.append(list(map(statistics.mean, zip(*aSlotLrandom))))
    parametersRandomMean.append(list(map(statistics.mean, zip(*parameterLrandom))))
    listSimulation.clear()
    listAfirst.clear()
    listRandom.clear()
    '''
#}
print(executionTimeMean)

'''    
tmpOutListSimulation = list(map(list, zip(*aParametersSimulationMean)))
tmpOutListArrivalFirst = list(map(list, zip(*parametersArrivalFirstMean)))
tmpOutListRandom = list(map(list, zip(*parametersRandomMean)))

outListParameters = [variable] + tmpOutListSimulation + tmpOutListArrivalFirst + tmpOutListRandom
outListSlots = aSlotSimulationMean + aSlotArrivalFirstMean + aSlotRandomMean
print(outListParameters)
print(outListSlots)

with open("outputParameters.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(outListParameters)

with open("outputSlots.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(outListSlots)

'''

      


