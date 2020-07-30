#!/usr/bin/env python

import csv
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy import signal
import pandas as pd

#plots the measured tide relative to the expected tide for a particular gauge
def plotgauge(tidedifference,minimumt=0,maximumt=0,tshift=0,fignumber=1,title="",filterbool=True):
    dt = 5
    t = range(0,len(tidedifference)*dt,dt)
    minimumi = minimumt/dt
    if maximumt==0:
        maximumi = len(tidedifference)
    else:
        maximumi = maximumt/dt

    if filterbool==False:
        plt.figure(fignumber)
        plt.title(title)
        plt.xlabel("Time since beginning of event (minutes)")
        plt.ylabel("Water Height (meters)")
        time = t[minimumi:maximumi]
        for k in range(len(time)):
            time[k] = (time[k]-tshift)/60.0
        plt.plot(time,tidedifference[minimumi:maximumi],"b")
    else:
        newbounds = tidedifference[minimumi:maximumi]
        for i in range(len(newbounds)):
            if np.isnan(newbounds[i]):
                newbounds[i]=0

        filtered = filterdata(newbounds,1)
        
        plt.figure(fignumber)
        plt.title(title)
        plt.plot(t[minimumi:maximumi],filtered,"b")
        #filtered = filterdata(newbounds,0.015)
        #plt.plot(t[minimumi:maximumi],filtered,"black")

#plots the measured tide relative to the expected tide for a particular gauge
def plotDART(time,tidedifference,minimumt=0,maximumt=0,tshift=0,fignumber=1,title="",filterbool=True):

    minimumi = int(minimumt/(time[1]-time[0]))
    maximumi = int(maximumt/(time[1]-time[0]))
    
    if filterbool==False:
        plt.figure(fignumber)
        plt.title(title)
        plt.xlabel("Time since beginning of event (minutes)")
        plt.ylabel("Water Height (meters)")
        time = time[minimumi:maximumi]
        for k in range(len(time)):
            time[k] = (time[k]-tshift)/60
        plt.plot(time,tidedifference[minimumi:maximumi],"b")
    else:
        newbounds = tidedifference[minimumi:maximumi]
        for i in range(len(newbounds)):
            if np.isnan(newbounds[i]):
                newbounds[i]=0

        filtered = filterdata(newbounds,1)
        
        plt.figure(fignumber)
        plt.title(title)
        plt.plot(t[minimumi:maximumi],filtered,"b")
        #filtered = filterdata(newbounds,0.015)
        #plt.plot(t[minimumi:maximumi],filtered,"black")

#plots the simulatino results of Tony Song's simulation
def plotTony(timelist,levellist,tshift=0,fignumber=1,color="green"):
    timelist2 = np.copy(timelist)
    for i in range(len(timelist2)):
        timelist2[i] = (timelist2[i]+tshift)/60
    plt.figure(fignumber)
    plt.plot(timelist2,levellist,color)

#plots tsunami squares data 
def plotTS(timelist,levellist,tshift=0,fignumber=1,color="green"):
    timelist2 = np.copy(timelist)
    maxx = 0
    maxxi = 0
    for i in range(len(timelist2)):
        if (levellist[i]>maxx):
            maxx=levellist[i]
            maxxi=i
        timelist2[i] = (timelist2[i]+tshift)/60

    print(maxxi,maxx,timelist[maxxi],timelist2[maxxi])
    nc = len(timelist2)
    cutoff = 1
    filtered = filterdata(levellist,cutoff)
    plt.figure(fignumber)
    plt.plot(timelist2,filtered,color)

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
                time.append(line[i][1])
                date.append(line[i][0])
    for i in range(len(tide)):
        tidediff.append(tide[i]-exptide[i])

    return tidedev

#returns the sim time, level, lat, and lon arrays from the selected simulation filename
def getsimdata(filename):
    #TSfilename = "/home/davidgrzan/Tsunami/Tohoku/output/"+filename
    TSfilename = "/home/davidgrzan/Tsunami/Maule/output/"+filename
    
    #pulling Tsunami Squares data from the netCDF output file
    simdata = Dataset(TSfilename, "r", format="NETCDF4")
    simtime = np.array(simdata.variables['time'])
    simlevel = np.array(simdata.variables['level'])
    #simheight = np.array(simdata.variables['height'])
    #simaltitude = np.array(simdata.variables['altitude'])
    simlatitude = np.array(simdata.variables['latitude'])
    simlongitude = np.array(simdata.variables['longitude'])

    return simtime, simlevel, simlatitude, simlongitude

def gettonydata(filename):
    #TSfilename = "/home/davidgrzan/Tsunami/Tohoku/output/"+filename
    TSfilename = filename

    simdata = Dataset(TSfilename, "r", format="NETCDF4")
    #simtime = np.array(simdata.variables['time_step'])
    simtime = np.array(simdata.variables['scrum_time'])
    simlevel = np.array(simdata.variables['zeta'])

    return simtime, simlevel

def getDARTdata(whichgauge):
    filename = "/home/davidgrzan/Tsunami/Tohoku/NOWPHAS_Tsunami_data/"+whichgauge+".txt"
    tidediff = []
    total = []
    seconds = []
    minutes = []
    hours = []
    days = []
    
    with open(filename) as file:
        line = list(csv.reader(file,delimiter="\t"))
        fill = False
        for i in range(len(line)):
            second = float(line[i][6])
            minute = float(line[i][5])
            hour = float(line[i][4])
            day = float(line[i][3])
            if day==11 and hour==4 and minute==0 and second==0:
                fill = True
            if fill==True:    
                tidediff.append(float(line[i][9]))
                days.append(day)
                hours.append(hour)
                minutes.append(minute)
                seconds.append(second)

    offset = 11*24*60*60+4*60*60
    for i in range(len(seconds)):
        totalcount=0
        totalcount+=seconds[i]
        totalcount+=minutes[i]*60
        totalcount+=hours[i]*60*60
        totalcount+=days[i]*24*60*60
        total.append(totalcount-offset)

    return total, tidediff

def getDARTdata2(whichgauge):
    filename = "/home/davidgrzan/Tsunami/Tohoku/NOWPHAS_Tsunami_data/"+whichgauge+".txt"
    tidediff = []
    total = []
    seconds = []
    minutes = []
    hours = []
    days = []
    
    with open(filename) as file:
        line = list(csv.reader(file,delimiter="\t"))
        fill = False
        for i in range(len(line)):
            second = float(line[i][6])
            minute = float(line[i][5])
            hour = float(line[i][4])
            day = float(line[i][3])
            if day==27 and hour==6 and minute==0 and second==0:
                fill = True
            if fill==True:    
                tidediff.append(float(line[i][9]))
                days.append(day)
                hours.append(hour)
                minutes.append(minute)
                seconds.append(second)

    offset = 27*24*60*60+6*60*60
    for i in range(len(seconds)):
        totalcount=0
        totalcount+=seconds[i]
        totalcount+=minutes[i]*60
        totalcount+=hours[i]*60*60
        totalcount+=days[i]*24*60*60
        total.append(totalcount-offset)

    return total, tidediff

#finds latitude and longitude array index that has value closest to the gauge lat and lon
def findlocation(latlist,lonlist,lat,lon):
    difflat = float('inf')
    difflon = float('inf')
    diff = 0
    latindex = 0
    lonindex = 0
    lonn = 0
    latt = 0
    for i in range(len(latlist)):
        diff = abs(lat-latlist[i])
        if diff<difflat:
            difflat = diff
            latindex = i
            latt = latlist[i]

    for i in range(len(lonlist)):
        diff = abs(lon-lonlist[i])
        if diff<difflon:
            difflon = diff
            lonindex = i
            lonn = lonlist[i]

    print(latt,lonn)
    return latindex, lonindex

#finds lat and lon array index from the bathymetry file tony uses
def findlocationtony(lon,lat):
    bathymetryfile = "/home/davidgrzan/Tsunami/Tohoku/bathymetry/Pacific_2400x1800.nc"
    bathymetrydata = Dataset(bathymetryfile, "r", format="NETCDF4")

    lonlist = np.array(bathymetrydata.variables['lon_u'])
    latlist = np.array(bathymetrydata.variables['lat_u'])
    lonlist = lonlist[0,:]
    latlist = latlist[:,0]

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

    return lonindex, latindex

#prints out the bathymetry height of tony's bathymetry and our bathymetry
def bathymetrycomparison(lonindex,latindex,lonindext,latindext):
    filet = "/home/davidgrzan/Tsunami/Tohoku/bathymetry/Pacific_2400x1800.nc"
    datat = Dataset(filet, "r", format="NETCDF4")
    heightt = np.array(datat.variables['h'])

    filename = "MidJapanGPS.nc"
    TSfilename = "/home/davidgrzan/Tsunami/Tohoku/output/"+filename
    simdata = Dataset(TSfilename, "r", format="NETCDF4")
    simheight = np.array(simdata.variables['altitude'])

    ht = heightt[latindext,lonindext]
    hm = -1*simheight[0,latindex,lonindex]
    
    print(heightt[latindext,lonindext])
    print(-1*simheight[0,latindex,lonindex])
    print(abs(ht-hm)/hm)
    print("\n")
    
#low pass filter
def filterdata(data, cutoff):
    b, a = signal.butter(5, cutoff, "low")
    output = signal.filtfilt(b,a,data)
    return output
    

if __name__ == "__main__":

    #ADJUSTABLE PARAMETERS
    gaugelistG = ["801G","802G","803G","804G","806G","807G","811G","812G","813G","815G"]
    gaugelistT = ["202T","203T","217T","219T","221T","315T","316T","317T","318T","319T","407T","419T","504T","507T","618T","624T","625T","626T","901T"]
    gaugelistW = ["202W","203W","205W","219W","301W","307W","308W","309W","320W","411W","501W","504W","602W","613W","901W"]
    
    """
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
    TSfilename = "MomentumTransferTest_0.025fac.nc"
    gaugelat = 36.9713
    gaugelon = 141.1855
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=54000-224,fignumber=1,color="red")

    #806G TS
    TSfilename = "MomentumTransferTest_0.010fac.nc"
    gaugelat = 36.9713
    gaugelon = 141.1855
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=54000-224,fignumber=1,color="orange")
    """
    """
    #plotting a variety of different factor values~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    factors = ["-0.015","-0.010","-0.005","0","0.001","0.005","0.010","0.025"]

    #802 gauge
    jet = plt.get_cmap("jet")
    colors = iter(jet(np.linspace(0,1,len(factors))))
    
    fig10 = plt.figure(10,figsize=(15,7))
    ax0 = fig10.add_subplot(1,1,1)
    ax0.set_title("802G")
    ax0.set_xlabel("Time (s)")
    ax0.set_ylabel("Water Level (m)")
    
    whichgauge = "802G"
    tidediff = getgaugedata(whichgauge)
    t = range(0,len(tidediff)*5,5)
    ax0.plot(t[50000/5:57000/5],tidediff[50000/5:57000/5],label="Gauge Data",color="black")

    for val in factors:
        TSfilename = "NorthMomentumTest_{}fac.nc".format(str(val))
        gaugelat = 39.2586
        gaugelon = 142.0969 
        simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
        latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
        for i in range(len(simtime)):
            simtime[i] = simtime[i]+53500+190
        ax0.plot(simtime,simlevel[:,latindex,lonindex],color=next(colors),label="Factor: {}".format(str(val)))

    ax0.legend()

    #801 gauge
    jet = plt.get_cmap("jet")
    colors = iter(jet(np.linspace(0,1,len(factors))))
    
    fig11 = plt.figure(11,figsize=(15,7))
    ax1 = fig11.add_subplot(1,1,1)
    ax1.set_title("801G")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Water Level (m)")
    
    whichgauge = "801G"
    tidediff = getgaugedata(whichgauge)
    t = range(0,len(tidediff)*5,5)
    ax1.plot(t[135000/5:143500/5],tidediff[135000/5:143500/5],label="Gauge Data",color="black")

    for val in factors:
        TSfilename = "NorthMomentumTest_{}fac.nc".format(str(val))
        gaugelat = 38.2325
        gaugelon = 141.6836
        simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
        latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
        for i in range(len(simtime)):
            simtime[i] = simtime[i]+140000
        ax1.plot(simtime,simlevel[:,latindex,lonindex],color=next(colors),label="Factor: {}".format(str(val)))

    ax1.legend()

    #803 gauge
    jet = plt.get_cmap("jet")
    colors = iter(jet(np.linspace(0,1,len(factors))))
    
    fig12 = plt.figure(12,figsize=(15,7))
    ax2 = fig12.add_subplot(1,1,1)
    ax2.set_title("803G")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Water Level (m)")
    
    whichgauge = "803G"
    tidediff = getgaugedata(whichgauge)
    t = range(0,len(tidediff)*5,5)
    ax2.plot(t[139000/5:143000/5],tidediff[139000/5:143000/5],label="Gauge Data",color="black")

    for val in factors:
        TSfilename = "NorthMomentumTest_{}fac.nc".format(str(val))
        gaugelat = 38.8577
        gaugelon = 141.8944
        simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
        latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
        for i in range(len(simtime)):
            simtime[i] = simtime[i]+140000+109
        ax2.plot(simtime,simlevel[:,latindex,lonindex],color=next(colors),label="Factor: {}".format(str(val)))

    ax2.legend()
    """
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #802G gauge
    whichgauge = "802G"
    tidediff = getgaugedata(whichgauge)
    plotgauge(tidediff,minimumt=50000,maximumt=64000,fignumber=2,title=whichgauge)

    #802G tony simulation
    latindex = 532
    lonindex = 1378
    simtimet, simlevelt = gettonydata("Japan_tsunami30s_gps_P1V1_NBPn6.nc")
    print(simtimet[0],simtimet[1],simtimet[2])
    time802 = np.copy(simtimet)
    level802 = simlevelt[:,1365,521]
    plotTony(time802,level802,tshift=53160,fignumber=2,color="green")
    
    """
    #802G TS
    TSfilename = "Wavespeed_0.66.nc"
    gaugelat = 39.2586
    gaugelon = 142.0969 
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=53160,fignumber=2,color="red")

    #802G TS
    TSfilename = "Wavespeed_0.6.nc"
    gaugelat = 39.2586
    gaugelon = 142.0969
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=53160,fignumber=2,color="green")

    #802G TS
    TSfilename = "Wavespeed_0.55.nc"
    gaugelat = 39.2586
    gaugelon = 142.0969 
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=53160,fignumber=2,color="orange")
    
    #802G TS
    TSfilename = "Wavespeed_0.5.nc"
    gaugelat = 39.2586
    gaugelon = 142.0969 
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=53160,fignumber=2,color="purple")
    
    #802G TS
    TSfilename = "Wavespeed_0.45.nc"
    gaugelat = 39.2586
    gaugelon = 142.0969 
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=53160,fignumber=2,color="black")
    """
    """
    #802G TS
    TSfilename = "NorthMomentumTest_0.025fac.nc"
    gaugelat = 39.2586
    gaugelon = 142.0969 
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=53500+190,fignumber=2,color="red")
    
    #802G TS
    TSfilename = "NorthMomentumTest_0.010fac.nc"
    gaugelat = 39.2586
    gaugelon = 142.0969 
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=53500+190,fignumber=2,color="orange")

    #802G TS
    TSfilename = "NorthMomentumTest_-0.010fac.nc"
    gaugelat = 39.2586
    gaugelon = 142.0969 
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=53500+190,fignumber=2,color="black")
    """
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #801G gauge
    whichgauge = "801G"
    tidediff = getgaugedata(whichgauge)
    plotgauge(tidediff,minimumt=135000,maximumt=143500,fignumber=3,title=whichgauge)

    time801 = np.copy(simtimet)
    level801 = simlevelt[:,1366,527]
    plotTony(time801,level802,tshift=139560,fignumber=3,color="green")
    
    """
    #801G TS
    TSfilename = "Wavespeed_0.66.nc"
    gaugelat = 38.2325
    gaugelon = 141.6836
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=3,color="red")

    #801G TS
    TSfilename = "Wavespeed_0.6.nc"
    gaugelat = 38.2325
    gaugelon = 141.6836
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=3,color="green")

    #801G TS
    TSfilename = "Wavespeed_0.55.nc"
    gaugelat = 38.2325
    gaugelon = 141.6836
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=3,color="orange")
    
    #801G TS
    TSfilename = "Wavespeed_0.5.nc"
    gaugelat = 38.2325
    gaugelon = 141.6836
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=3,color="purple")
    
    #801G TS
    TSfilename = "Wavespeed_0.45.nc"
    gaugelat = 38.2325
    gaugelon = 141.6836
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=3,color="black")
    """
    """
    #801G TS
    TSfilename = "NorthMomentumTest_0.025fac.nc"
    gaugelat = 38.2325
    gaugelon = 141.6836
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=140000,fignumber=3,color="red")

    #801G TS
    TSfilename = "NorthMomentumTest_0.010fac.nc"
    gaugelat = 38.2325
    gaugelon = 141.6836
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=140000,fignumber=3,color="orange")

    #801G TS
    TSfilename = "NorthMomentumTest_-0.010fac.nc"
    gaugelat = 38.2325
    gaugelon = 141.6836
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=140000,fignumber=3,color="black")
    """
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #803G gauge
    whichgauge = "803G"
    tidediff = getgaugedata(whichgauge)
    plotgauge(tidediff,minimumt=139000,maximumt=143000,fignumber=4,title=whichgauge)

    time803 = np.copy(simtimet)
    level803 = simlevelt[:,1373,529]
    plotTony(time803,level802,tshift=139560,fignumber=4,color="green")
    
    """
    #803G TS
    TSfilename = "Wavespeed_0.66.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=4,color="red")

    #803G TS
    TSfilename = "Wavespeed_0.6.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=4,color="green")

    #803G TS
    TSfilename = "Wavespeed_0.55.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=4,color="orange")
    
    #803G TS
    TSfilename = "Wavespeed_0.5.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=4,color="purple")
    
    #803G TS
    TSfilename = "Wavespeed_0.45.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=4,color="black")
    """
    """
    #803G TS
    TSfilename = "NorthMomentumTest_0.025fac.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=140000+109,fignumber=4,color="red")

    #803G TS
    TSfilename = "NorthMomentumTest_0.010fac.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=140000+109,fignumber=4,color="orange")

    #803G TS
    TSfilename = "NorthMomentumTest_-0.010fac.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime,simlevel[:,latindex,lonindex],tshift=140000+109,fignumber=4,color="black")
    """
    """
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
    """
    """
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #803G gauge
    whichgauge = "803G"
    tidediff = getgaugedata(whichgauge)
    plotgauge(tidediff,minimumt=139000,maximumt=143000,fignumber=6,title=whichgauge)
    
    #803G TS
    TSfilename = "MidJapanBigEQ_dip5_0.25x.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime[:400],simlevel[:400,latindex,lonindex],tshift=140000,fignumber=6,color="brown")

    #803G TS
    TSfilename = "MidJapanBigEQ_dip10_0.25x.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = getsimdata(TSfilename)
    latindex, lonindex = findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    plotTS(simtime[:400],simlevel[:400,latindex,lonindex],tshift=140000,fignumber=6,color="yellow")

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
    """
    fn = 4
    for name in gaugelistG:
        tidediff = getgaugedata(name)
        plotgauge(tidediff,fignumber=fn,title=name)
        fn+=1
    """
    #plotting
    plt.show()
    

    
    
    
