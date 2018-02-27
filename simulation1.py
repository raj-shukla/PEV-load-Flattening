import math
import csv
from operator import itemgetter
import random
import statistics
import copy
from datetime import datetime
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

    
    print(netPower)
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
    print(netPower)
    print(parameters)

    print(aSchedule)
    
    
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
                            print("############")
                            print(j)
                            print(pReduce)
                            print(netPower[sSlot:aSchedule[j][1] + aSchedule[j][2]])
                            print(netPower[sSlot:eSlot])
                            print(netPower[sSlot:aSchedule[j][1] + aSchedule[j][2]])
                            print(netPower[sSlot:eSlot])
                            netPower[sSlot:aSchedule[j][1] + aSchedule[j][2]] = list(map(lambda x: x - pReduce, netPower[sSlot:aSchedule[j][1] + aSchedule[j][2]]  ))
                            netPower[sSlot:eSlot] = list(map(lambda x: x + pIncrease, netPower[sSlot:eSlot]))
                            print(FindValues(netPower[:])[1:])
                            print(aSchedule[j])
                            print(aSchedule[j][1] + aSchedule[j][2] - sSlot)
                            print(nSlot)
                            print(eSlot - sSlot)
                            print(netPower[sSlot:aSchedule[j][1] + aSchedule[j][2]])
                            print(netPower[sSlot:eSlot])
                            print( sum(netPower))
                            aSchedule[j][2] = nSlot
                            aSchedule[j][4] =  3
                            print(netPower[sSlot:aSchedule[j][1] + aSchedule[j][2]])
                            print(netPower[sSlot:eSlot])
                            print(sum(netPower))
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
                            print("#######################")
                            print(aSchedule[j])
                            print(netPower[sSlot:aSchedule[j][1] + aSchedule[j][2]])
                            print( netPower[sSlot:eSlot])
                            print(dSlot)
                            print(eSlot)
                            netPower[sSlot:aSchedule[j][1] + aSchedule[j][2]] = list(map(lambda x: x - pReduce, netPower[sSlot:aSchedule[j][1] + aSchedule[j][2]]  ))
                            netPower[sSlot:eSlot] = list(map(lambda x: x + pIncrease, netPower[sSlot:eSlot]))
                            print(FindValues(netPower[:])[1:])
                            print(aSchedule[j][1] + aSchedule[j][2]- sSlot)
                            print(nSlot)
                            print(eSlot - sSlot)
                            print(netPower[sSlot:aSchedule[j][1] + aSchedule[j][2]] )
                            print( netPower[sSlot:eSlot])
                            print(sum(netPower))
                            aSchedule[j][2] = nSlot
                            aSchedule[j][4] =  1
                    #}
                #}
                #}
            #}
        #}
        #print("###################################################")
        lIndexList.clear()
        lIndexList = [[], []]
        lStartIndex = 0
        lEndIndex = 0
        #print(netPower)
        
        
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

        #print(netPower)
        #print(averagePower)
        #print(lIndexList)
        
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
                   print("######################################")
                   print(aSchedule[j])
                   print(FindValues(netPower[:])[1:])
                   print(netPower[sSlot:sSlot + nSlot])
                   print(netPower[dSlot - nSlot + 1:dSlot + 1])
                   print(aPower)
                   print(sSlot)
                   print(nSlot)
                   print(dSlot - nSlot + 1)
                   print(dSlot)
                   netPower[sSlot:sSlot + nSlot] = list(map(lambda x: x - aPower, netPower[sSlot:sSlot + nSlot]  ))
                   netPower[dSlot - nSlot + 1:dSlot + 1] = list(map(lambda x: x + aPower, netPower[dSlot - nSlot + 1:dSlot + 1]))
                   print(netPower[sSlot:sSlot + nSlot])
                   print(netPower[dSlot - nSlot + 1:dSlot + 1])
                   print(sum(netPower))
                   aSchedule[j][1] = dSlot - nSlot + 1
                #}
            #}
        #}

        
        parameters = FindValues(netPower[:])
        if(parameters[5] <= Alist[5]):
        #{
            print("##############################################################################")
            Alist = parameters[:]
            #print(parameters)
            print(Alist)
            print(aSchedule)
        #}
        
    #}
    print(parameters)
    print(Alist)
    #print(aSchedule)
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
        #print("###########################")
        #print(arrivalSlot)
        #print(slotsToCharge)
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
    #print("##################################################################################")
    #print(parameters)
    #print(netPower)
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
        #print("###########################")
        #print(arrivalSlot)
        #print(slotsToCharge)
        #print(departureSlot)
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
    #print("##################################################################################")
    #print(parameters)
    #print(netPower)
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

for i in range(0, 1):
#{
    for i in range(0, 1):
    #{
        simulationData = simulation_data.SimulationData()
        listSimulation.append(Simulation(simulationData))
        #listAfirst.append(SimulationArrivalFirst(simulationData))
        #listRandom.append(SimulationRandom(simulationData)) 
    #}
    aSlotLsimulation = [i[0] for i in listSimulation]
    parameterLsimulation = [i[1:] for i in listSimulation]
    print(parameterLsimulation)
    aSlotSimulationMean.append(list(map(statistics.mean, zip(*aSlotLsimulation))))
    aParametersSimulationMean.append(list(map (statistics.mean, zip(*parameterLsimulation))))
    aSlotLarrivalFirst = [i[0] for i in listAfirst]
    parameterLarrivalFirst = [i[1:] for i in listAfirst]
    print(parameterLarrivalFirst)
    aSlotArrivalFirstMean.append(list(map(statistics.mean, zip(*aSlotLarrivalFirst))))
    parametersArrivalFirstMean.append(list(map(statistics.mean, zip(*parameterLarrivalFirst))))
    aSlotLrandom = [i[0] for i in listRandom]
    parameterLrandom = [i[1:] for i in listRandom]
    print(parameterLrandom)
    aSlotRandomMean.append(list(map(statistics.mean, zip(*aSlotLrandom))))
    parametersRandomMean.append(list(map(statistics.mean, zip(*parameterLrandom))))
    listSimulation.clear()
    listAfirst.clear()
    listRandom.clear()
#}

#print(aSlotSimulationMean)
print(aParametersSimulationMean)
#print(aSlotArrivalFirstMean)
print(parametersArrivalFirstMean)
#print(aSlotRandomMean)
print(parametersRandomMean)

      


