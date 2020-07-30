#!/usr/bin/env python

import csv
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy import signal
import gaugecomparison as g

if __name__ == "__main__":

    simtimet, simlevelt = g.gettonydata("Japan_tsunami30s_gps_P1V1_NBPn6.nc")
    """
    #801G ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "801G"
    tidediff = g.getgaugedata(whichgauge)
    g.plotgauge(tidediff,minimumt=138000,maximumt=149000,tshift=139560,fignumber=1,title=whichgauge,filterbool=False)

    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 38.2325
    gaugelon = 141.6836

    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    simtimet, simlevelt = g.gettonydata("Japan_tsunami30s_gps_P1V1_NBPn6.nc")
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=0,fignumber=1,color="green")

    
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    print(latindex,lonindex)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=0,fignumber=1,color="red")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)
    
    #802G ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "802G"
    tidediff = g.getgaugedata(whichgauge)
    g.plotgauge(tidediff,minimumt=50000,maximumt=63000,tshift=53160,fignumber=2,title=whichgauge,filterbool=False)

    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 39.2586
    gaugelon = 142.0969

    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=0,fignumber=2,color="green")

    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=0,fignumber=2,color="red")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)
    
    #803G ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "803G"
    tidediff = g.getgaugedata(whichgauge)
    g.plotgauge(tidediff,minimumt=138000,maximumt=149000,fignumber=3,title=whichgauge,filterbool=False)

    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 38.8577
    gaugelon = 141.8944
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=3,color="red")

    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=139560,fignumber=3,color="green")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)

    #804G ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "804G"
    tidediff = g.getgaugedata(whichgauge)
    g.plotgauge(tidediff,minimumt=50000,maximumt=63000,fignumber=4,title=whichgauge,filterbool=False)

    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 39.627222
    gaugelon = 142.096944
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=53160,fignumber=4,color="red")

    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext+1],tshift=53160,fignumber=4,color="green")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)
    
    #806G ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "806G"
    tidediff = g.getgaugedata(whichgauge)
    g.plotgauge(tidediff,minimumt=50000,maximumt=63000,fignumber=5,title=whichgauge,filterbool=False)

    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 36.9714
    gaugelon = 141.18555
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=53160,fignumber=5,color="red")

    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=53160,fignumber=5,color="green")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)
    
    #807G ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "807G"
    tidediff = g.getgaugedata(whichgauge)
    g.plotgauge(tidediff,minimumt=50000,maximumt=63000,fignumber=6,title=whichgauge,filterbool=False)

    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 40.1166666
    gaugelon = 142.06666
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=53160,fignumber=6,color="red")

    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=53160,fignumber=6,color="green")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)
    
    #205W ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "205W"
    tidediff = g.getgaugedata(whichgauge)
    g.plotgauge(tidediff,minimumt=138000,maximumt=149000,fignumber=7,title=whichgauge,filterbool=False)

    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 38.25
    gaugelon = 141.0661
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=7,color="red")

    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=139560,fignumber=7,color="green")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)
    
    #219W ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "219W"
    tidediff = g.getgaugedata(whichgauge)
    g.plotgauge(tidediff,minimumt=138000,maximumt=149000,fignumber=8,title=whichgauge,filterbool=False)

    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 40.0913
    gaugelon = 141.871
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=8,color="red")

    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext+2],tshift=139560,fignumber=8,color="green")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)
    
    #202W ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "202W"
    tidediff = g.getgaugedata(whichgauge)
    g.plotgauge(tidediff,minimumt=138000,maximumt=149000,fignumber=9,title=whichgauge,filterbool=False)

    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 40.925
    gaugelon = 141.42416
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=9,color="red")

    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=139560,fignumber=9,color="green")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)
    
    #203T ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "203T"
    tidediff = g.getgaugedata(whichgauge)
    g.plotgauge(tidediff,minimumt=138000,maximumt=149000,fignumber=10,title=whichgauge,filterbool=False)

    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 40.55
    gaugelon = 141.55555
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=10,color="red")

    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext+1,lonindext],tshift=139560,fignumber=10,color="green")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)
    
    #TM1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "TM1"

    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 39.25
    gaugelon = 142.768
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=11,color="red")
    
    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=139560,fignumber=11,color="green")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)

    #TM2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "TM2"
    
    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 39.250
    gaugelon = 142.445
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=139560,fignumber=12,color="red")

    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=139560,fignumber=12,color="green")

    print(whichgauge)
    g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)
    """
    #DT21413 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "DT21413"
    timee, tidediff = g.getDARTdata(whichgauge)
    g.plotDART(timee, tidediff, minimumt=0, maximumt=30000, tshift=6360, fignumber=13, title=whichgauge, filterbool=False)

    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 30.515
    gaugelon = 152.117#-180

    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime[:int(len(simtime)*0.9)],simlevel[:int(len(simtime)*0.9),latindex,lonindex],tshift=0,fignumber=13,color="red")

    gaugelon = 152.117
    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=0,fignumber=13,color="green")

    print(whichgauge)
    #g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)
    
    #DT21401 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "DT21401"
    timee, tidediff = g.getDARTdata(whichgauge)
    g.plotDART(timee, tidediff, minimumt=0, maximumt=30000, tshift=6360, fignumber=14, title=whichgauge, filterbool=False)
    
    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 42.617
    gaugelon = 152.583#-180

    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=0,fignumber=14,color="red")
    
    gaugelon = 152.583
    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=0,fignumber=14,color="green")

    print(whichgauge)
    #g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)

    #DT21418 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "DT21418"
    timee, tidediff = g.getDARTdata(whichgauge)
    g.plotDART(timee, tidediff, minimumt=0, maximumt=25000, tshift=6360, fignumber=15, title=whichgauge, filterbool=False)
    
    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 38.711
    gaugelon = 148.694#-180
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime,simlevel[:,latindex,lonindex],tshift=0,fignumber=15,color="red")

    gaugelon = 148.694
    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=0,fignumber=15,color="green")

    print(whichgauge)
    #g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)

    """
    #DT51407 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    whichgauge = "DT51407"
    timee, tidediff = g.getDARTdata(whichgauge)
    g.plotDART(timee, tidediff, minimumt=0, maximumt=80000, fignumber=16, title=whichgauge, filterbool=False)
    
    TSfilename = "Tohoku_GPSNEW3.nc"
    gaugelat = 19.620
    gaugelon = -156.511+180
    simtime, simlevel, simlatitude, simlongitude = g.getsimdata(TSfilename)
    latindex, lonindex = g.findlocation(simlatitude,simlongitude,gaugelat,gaugelon)
    g.plotTS(simtime[:],simlevel[:,latindex,lonindex],tshift=6360,fignumber=16,color="red")

    gaugelon = -156.511+360
    lonindext, latindext = g.findlocationtony(gaugelon,gaugelat)
    #g.plotTony(simtimet,simlevelt[:,latindext,lonindext],tshift=6360,fignumber=16,color="green")

    print(whichgauge)
    #g.bathymetrycomparison(lonindex,latindex,lonindext,latindext)
    """
    
    plt.show()
