#!/usr/bin/python2.7

#revised 11/3/2017

import time
import PHDLibraries
import math

#time.strftime("%H:%M:%S")
#captureCamera('11/3/2017')

start = time.time()

#Initialize variables
state=0
distFreq=100    #take a distance sensor measurement every distFreq accel measurements
GPSFreq=50000   #take a gps every GPSFreq accel measurements
x=1
x2=0
x2Max=100
trigger=0
dist=0
accelTriggerLow=250
accelTriggerHigh=350
distTriggerLow=700
distTriggerHigh=700
dist2=0

picName="pic"
picCounter=0

#accelRunningAverage=PHDLibraries.runningAverage(count2)
#distRunningAverage=PHDLibraries.flat_filter()
distf=PHDLibraries.flat_filter()
triggerFileName='trigger'
roughnessFileName='roughness'

while True:
    triggered=False
    
    #state 0 handles file initialization
    if (state==0):
        #timeStr=time.strftime("%Y%m%d%H%M")
        timeStr= 'Now_Nov_30_2017'
        temp = triggerFileName + timeStr
        triggerFile = open( temp , 'w')
        temp = roughnessFileName + timeStr
        roughnessFile = open( temp , 'w')
        picCounter=0
        state=1
    
    #state 1 handles the pot hole triggering system and the roughness detector
    if (state==1):
        if (x%GPSFreq==1):
            gps=PHDLibraries.captureGPS()
            roughnessFile.write(str(gps)+time.strftime("%c")+"\n")

        z=PHDLibraries.captureAccel()
        if ((z>accelTriggerHigh)|(z<accelTriggerLow)):
            trigger=1
            state=2
            #for measuring pot hole severity we need
            # to reset min and max measurements
            zHighest=300
            zLowest=300
        else:
            trigger=0

        if (x%distFreq==0):
            dist=PHDLibraries.captureDistance()
            dist2=distf.filter_dl(dist)

        #write to file operations for roughness indicator
        roughnessFile.write(str(x)+" "+str(z)+" "+str(dist)+" "+str(trigger)+" "+str(dist2)+"\n")

        #This is to close the files before they cause a crash
        if (x>=100000):
            triggerFile.close()
            roughnessFile.close()
            state=0
        x +=1
    
    #state 2 handles events once the system has been triggered
    if (state==2):
        xMax=x+2000
        trigger=2

        z=PHDLibraries.captureAccel()
        if (z>zHighest):
            zHighest = z
        if (z < zLowest):
            zLowest = z


        dist=PHDLibraries.captureDistance()
        dist2=distf.filter_dl(dist)
        if ((dist<dist2-distTriggerLow)|(dist>dist2+distTriggerHigh)|(x>xMax)):
            PHDLibraries.captureCamera(picName+timeStr+str(picCounter)+".png")
            picCounter+=1
            state=1
            gps2 = PHDLibraries.captureGPS()
            severity = (zHighest - zLowest)/150
            triggerFile.write(str(gps) +' ' + str(gps2)+ ' '+ str(severity) + ' ' + picName+timeStr+str(picCounter)+".png" +'\n') 
        x +=1

    if (trigger>=1):
        print '***loop completed, pothole detected'
    else:
        #print 'loop completed, no pothole detected'
        nothing=0
