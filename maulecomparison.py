#!/usr/bin/env python

import csv
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy import signal
import gaugecomparison as g

if __name__ == "__main__":

    simtimet, simlevelt = g.gettonydata("/home/davidgrzan/Tsunami/Maule/output/Chile_Sladen240s_source5.nc")

    #DT32412 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "DT32412"
    timee, tidediff = g.getDARTdata2(whichgauge)
    g.plotDART(timee, tidediff, minimumt=0, maximumt=30000, tshift=2051, fignumber=1, title=whichgauge, filterbool=False)

    TSfilename = "MauleDART3.nc"
    gaugelat = -17.975
    gaugelon = -86.3920

    lonindext, latindext = g.findlocationtony(gaugelon+360,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=0,fignumber=1,color="green")
    
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=0,fignumber=1,color="red")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)
    
    #DT51406 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "DT51406"
    timee, tidediff = g.getDARTdata2(whichgauge)
    g.plotDART(timee, tidediff, minimumt=0, maximumt=35000, tshift=2051, fignumber=2, title=whichgauge, filterbool=False)
    
    TSfilename = "MauleDART3.nc"
    gaugelat = -8.4925
    gaugelon = -125.0214
    
    lonindext, latindext = g.findlocationtony(gaugelon+360,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=0,fignumber=2,color="green")

    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=0,fignumber=2,color="red")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)

    #DT32411 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "DT32411"
    timee, tidediff = g.getDARTdata2(whichgauge)
    g.plotDART(timee, tidediff, minimumt=0, maximumt=50000, tshift=2051, fignumber=3, title=whichgauge, filterbool=False)
    
    TSfilename = "MauleDART3.nc"
    gaugelat = 4.9242
    gaugelon = -90.6858
    
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=0,fignumber=3,color="red")

    lonindext, latindext = g.findlocationtony(gaugelon+360,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=0,fignumber=3,color="green")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)
    
    
    plt.show()
