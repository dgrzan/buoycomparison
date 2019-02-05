#!/usr/bin/env python

import csv
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

#plots the measured tide relative to the expected tide for a particular gauge
def plotgauge(tidedifference,minimumt=0,maximumt=0,fignumber=1):
    t = range(0,len(tidedifference)*5,5)
    minimumi = minimumt/5
    if maximumt==0:
        maximumi = len(tidedifference)/5
    else:
        maximumi = maximumt/5
    plt.figure(fignumber)
    plt.plot(t[minimumi:maximumi],tidedifference[minimumi:maximumi],"b")

#plots tsunami squares data 
def plotTS(timelist,levellist,tshift=0,fignumber=1):
    adjtime = []
    if tshift!=0:
        for i in range(len(timelist)):
            timelist[i] = timelist[i]+tshift
    plt.figure(fignumber)
    plt.plot(timelist,levellist,"g")
    

#finds latitude and longitude array index that has value closest to the gauge lat and lon
def findlocation(latlist,lonlist,lat,lon):
    difflat = float('inf')
    difflon = float('inf')
    diff = 0
    latindex = 0
    lonindex = 0
    for i in range(len(latlist)):
        diff = abs(lat-latlist[i])
        if diff<difflat:
            difflat = diff
            latindex = i

    for i in range(len(lonlist)):
        diff = abs(lon-lonlist[i])
        if diff<difflon:
            difflon = diff
            lonindex = i

    return latindex, lonindex


if __name__ == "__main__":

    #ADJUSTABLE PARAMETERS
    gaugefilename = "/home/davidgrzan/Tsunami/Tohoku/NOWPHAS_Tsunami_data/2011TET219T.txt"
    TSfilename = "/home/davidgrzan/Tsunami/Tohoku/output/NorthernJapanEQ_dip5.nc"
    #gaugelat = 38.2325 #for 801
    #gaugelon = 141.6836 #for 801
    gaugelat = 40.1922
    gaugelon = 141.7966+0.2
    timeadjust = 141505
    mintime = 0#141000
    maxtime = 10000#143000

    #setting up array variables
    exptide = []     #astronomical tide level (expected tide with no influences except for gravitational bodies)
    tide = []     #measured tide level
    time = []
    date = []
    tidediff = []

    #opening the gauge file and setting lists
    with open(gaugefilename) as file:
        line = list(csv.reader(file, delimiter=","))
        for i in range(len(line)):
            if i>2:
                if float(line[i][2])==9999.99:
                    tide.append(float("nan"))
                else:
                    tide.append(float(line[i][2])/1000.0)
                exptide.append(float(line[i][3])/1000.0)
                time.append(line[i][1])
                date.append(line[i][0])

    for i in range(len(tide)):
        tidediff.append(tide[i]-exptide[i])
                
    #pulling Tsunami Squares data from the netCDF output file
    simdata = Dataset(TSfilename, "r", format="NETCDF4")
    simtime = np.array(simdata.variables['time'])
    simlevel = np.array(simdata.variables['level'])
    simheight = np.array(simdata.variables['height'])
    simaltitude = np.array(simdata.variables['altitude'])
    simlatitude = np.array(simdata.variables['latitude'])
    simlongitude = np.array(simdata.variables['longitude'])

    #finds lat and lon in lists that are closest to gauge location
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)

    #plotting
    plotgauge(tidediff,minimumt=mintime,maximumt=maxtime,fignumber=1)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=0,fignumber=2)
    plt.show()
    

    
    
    
