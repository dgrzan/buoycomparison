#!/usr/bin/env python

import csv
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

#plots the measured tide relative to the expected tide for a particular gauge
def plotgauge(tidedifference,minimumt=0,maximumt=0,fignumber=1,title=""):
    t = range(0,len(tidedifference)*5,5)
    minimumi = minimumt/5
    if maximumt==0:
        maximumi = len(tidedifference)
    else:
        maximumi = maximumt/5
    plt.figure(fignumber)
    plt.title(title)
    plt.plot(t[minimumi:maximumi],tidedifference[minimumi:maximumi],"b")

#plots tsunami squares data 
def plotTS(timelist,levellist,tshift=0,fignumber=1,color="green"):
    adjtime = []
    if tshift!=0:
        for i in range(len(timelist)):
            timelist[i] = timelist[i]+tshift
    plt.figure(fignumber)
    plt.plot(timelist,levellist,color)

#returns tide level array from the selected gauge
def getgaugedata(whichgauge):
    #setting up array variables
    exptide = []     #astronomical tide level (expected tide with no influences except for gravitational bodies)
    tide = []     #measured tide level
    time = []
    date = []
    tidedev = []
    tidediff = []
    gaugefilename = "/home/davidgrzan/Tsunami/Tohoku/NOWPHAS_Tsunami_data/2011TET"+whichgauge+".txt"

    #opening the gauge file and setting lists
    with open(gaugefilename) as file:
        line = list(csv.reader(file, delimiter=","))
        for i in range(len(line)):
            if i>2:
                if float(line[i][2])==9999.99:
                    tide.append(float("nan"))
                    tidedev.append(float("nan"))
                else:
                    tide.append(float(line[i][2])/100.0)
                    tidedev.append(float(line[i][4])/100.0)
                exptide.append(float(line[i][3])/100.0)
                #time.append(line[i][1])
                #date.append(line[i][0])
    for i in range(len(tide)):
        tidediff.append(tide[i]-exptide[i])

    return tidedev

#returns the sim time, level, lat, and lon arrays from the selected simulation filename
def getsimdata(filename):
    TSfilename = "/home/davidgrzan/Tsunami/Tohoku/output/"+filename
    
    #pulling Tsunami Squares data from the netCDF output file
    simdata = Dataset(TSfilename, "r", format="NETCDF4")
    simtime = np.array(simdata.variables['time'])
    simlevel = np.array(simdata.variables['level'])
    #simheight = np.array(simdata.variables['height'])
    #simaltitude = np.array(simdata.variables['altitude'])
    simlatitude = np.array(simdata.variables['latitude'])
    simlongitude = np.array(simdata.variables['longitude'])

    return simtime, simlevel, simlatitude, simlongitude

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
    gaugelistG = ["801G","802G","803G","804G","806G","807G","811G","812G","813G","815G"]
    gaugelistT = ["202T","203T","217T","219T","221T","315T","316T","317T","318T","319T","407T","419T","504T","507T","618T","624T","625T","626T","901T"]
    gaugelistW = ["202W","203W","205W","219W","301W","307W","308W","309W","320W","411W","501W","504W","602W","613W","901W"]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #806G gauge
    whichgauge = "806G"
    tidediff = getgaugedata(whichgauge)
    plotgauge(tidediff,minimumt=50000,maximumt=57500,fignumber=1,title=whichgauge)

    #806G TS
    TSfilename = "MidJapanEQ_dip5.nc"
    gaugelat = 36.9713
    gaugelon = 141.1855
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=54000-224,fignumber=1)

    #806G TS
    TSfilename = "MidJapanEQ_dip10.nc"
    gaugelat = 36.9713
    gaugelon = 141.1855
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=54000-224,fignumber=1,color="red")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #802G gauge
    whichgauge = "802G"
    tidediff = getgaugedata(whichgauge)
    plotgauge(tidediff,minimumt=50000,maximumt=57000,fignumber=2,title=whichgauge)
    
    #802G TS
    TSfilename = "MidJapanEQ_dip5.nc"
    gaugelat = 39.2586
    gaugelon = 142.0969 
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=53500+190,fignumber=2)

    #802G TS
    TSfilename = "MidJapanEQ_dip10.nc"
    gaugelat = 39.2586
    gaugelon = 142.0969 
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=53500+190,fignumber=2,color="red")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #801G gauge
    whichgauge = "801G"
    tidediff = getgaugedata(whichgauge)
    plotgauge(tidediff,minimumt=135000,maximumt=143500,fignumber=3,title=whichgauge)

    #801G TS
    TSfilename = "MidJapanEQ_dip5.nc"
    gaugelat = 38.2325
    gaugelon = 141.6836
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=140000,fignumber=3)

    #801G TS
    TSfilename = "MidJapanEQ_dip10.nc"
    gaugelat = 38.2325
    gaugelon = 141.6836
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=140000,fignumber=3,color="red")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #803G gauge
    whichgauge = "803G"
    tidediff = getgaugedata(whichgauge)
    plotgauge(tidediff,minimumt=139000,maximumt=143000,fignumber=4,title=whichgauge)

    #803G TS
    TSfilename = "MidJapanEQ_dip5.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime[:400],simlevel[:400,latindex,lonindex],tshift=140000+109,fignumber=4)

    #803G TS
    TSfilename = "MidJapanEQ_dip10.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime[:400],simlevel[:400,latindex,lonindex],tshift=140000+109,fignumber=4,color="red")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #205W gauge
    whichgauge = "205W"
    tidediff = getgaugedata(whichgauge)
    plotgauge(tidediff,minimumt=130000,maximumt=0,fignumber=5,title=whichgauge)

    #205W TS
    TSfilename = "MidJapanBigEQ_dip5_0.25x.nc"
    gaugelat = 38.25
    gaugelon = 141.0661
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=142500,fignumber=5)

    #205W TS
    TSfilename = "MidJapanBigEQ_dip10_0.25x.nc"
    gaugelat = 38.25
    gaugelon = 141.0661
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=142500,fignumber=5,color="red")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #803G TS
    TSfilename = "MidJapanBigEQ_dip5_0.25x.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime[:400],simlevel[:400,latindex,lonindex],tshift=140000,fignumber=6)

    #803G TS
    TSfilename = "MidJapanBigEQ_dip10_0.25x.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime[:400],simlevel[:400,latindex,lonindex],tshift=140000,fignumber=6)

    #803G TS
    TSfilename = "MidJapanBigEQ_dip5_0.5x.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=140000,fignumber=6,color="red")

    #803G TS
    TSfilename = "MidJapanBigEQ_dip5.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=140000,fignumber=6,color="blue")
    
    #803G TS
    TSfilename = "MidJapanBigEQ_dip5_0.25x_ndiff1.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=140000,fignumber=6,color="black")
    
    #803G TS
    TSfilename = "MidJapanBigEQ_dip5_0.5x_ndiff.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=140000,fignumber=6,color="black")
    
    #803G TS
    TSfilename = "MidJapanBigEQ_dip5_0.25x_ndiff1.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=140000,fignumber=6,color="orange")
    
    """
    fn = 4
    for name in gaugelistG:
        tidediff = getgaugedata(name)
        plotgauge(tidediff,fignumber=fn,title=name)
        fn+=1
    """
    #plotting
    plt.show()
    

    
    
    
