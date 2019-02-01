#!/usr/bin/env python

import csv
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

if __name__ == "__main__":

    #ADJUSTABLE PARAMETERS
    gaugefilename = "/home/davidgrzan/Tsunami/Tohoku/NOWPHAS_Tsunami_data/2011TET801G.txt"
    gaugelat = 38.2325
    gaugelon = 141.6836
    timeadjust = 141505

    
    exptide = []     #astronomical tide level (expected tide with no influences except for gravitational bodies)
    tide = []     #measured tide level
    time = []
    date = []
    tidediff = []

    #opening the Mid Miyagi (801) GPS dataset, off the coast of sendai
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
    simdata = Dataset("/home/davidgrzan/Tsunami/Tohoku/output/TohokuEQ_dip5.nc", "r", format="NETCDF4")
    simtime = np.array(simdata.variables['time'])
    simlevel = np.array(simdata.variables['level'])
    simheight = np.array(simdata.variables['height'])
    simaltitude = np.array(simdata.variables['altitude'])
    simlatitude = np.array(simdata.variables['latitude'])
    simlongitude = np.array(simdata.variables['longitude'])
    
    #finding latitude and longitude array index that has value closest to the gauge lat and lon
    difflat = float('inf')
    difflon = float('inf')
    diff = 0
    latindex = 0
    lonindex = 0
    for i in range(len(simlatitude)):
        diff = abs(gaugelat-simlatitude[i])
        if diff<difflat:
            difflat = diff
            latindex = i

    for i in range(len(simlongitude)):
        diff = abs(gaugelon-simlongitude[i])
        if diff<difflon:
            difflon = diff
            lonindex = i

    print difflat
    print difflon
    print latindex
    print lonindex
    print simlatitude[latindex]
    print simlongitude[lonindex]
    print len(simlevel[:,0,0])
    print len(simtime)
    print len(simaltitude)

    #shifting TS time data over to match gauge time
    adjsimtime = []
    for i in range(len(simtime)):
        adjsimtime.append(simtime[i]+timeadjust)
        
    minr = 141000/5
    maxr = 143000/5
    t = range(0,len(date)*5,5)
    plt.figure(1)
    plt.plot(t[minr:maxr],tidediff[minr:maxr],"b")
    plt.plot(adjsimtime,simlevel[:,latindex,lonindex],"g")

    plt.figure(2)
    plt.plot(adjsimtime,simlevel[:,latindex,lonindex],"g")

    plt.show()
    
    
    
