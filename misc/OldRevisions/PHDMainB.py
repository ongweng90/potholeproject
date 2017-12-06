#!/usr/bin/python2.7

#revised 11/3/2017

import time
import PHDLibraries

#time.strftime("%H:%M:%S")
#captureCamera('11/3/2017')

start = time.time()
def sensorTest():
   print 'Accelerometer Test'
   z = PHDLibraries.captureAccel()
   print ('The Z axis value is %d' % (z))
   print '_______'
   print 'Distance sensor test'
   dist = PHDLibraries.captureDistance()
   print ('the distance is %d' % (dist))
   print '_______' 
   print 'GPS test'
   gpslist = PHDLibraries.captureGPS()
   print gpslist
   print '_______'
   message=time.strftime("%H:%M:%S") 
   PHDLibraries.lcdprint(message)
   print '_______'
   time.sleep(.5)

state=0
RACount=10
count1=1    #take a distance sensor measurement every count1 accel measurements
count2=50000   #take a gps every count2 accel measurements
x=1
x2=0
x2Max=100
trigger=0
dist=0
accelTriggerLow=250
accelTriggerHigh=350
distTriggerLow=5
distTriggerHigh=5000

#init_variables()    #standard init

accelRunningAverage=PHDLibraries.runningAverage(count2)
distRunningAverage=PHDLibraries.runningAverage(count2/count1)
#while (time.time() - start <= 1000):
while True:
    triggered=False

    if (state==0):
        baseLineDistList=PHDLibraries.runningAverage(RACount)
        for y in (0, RACount-1):
            baseLineDistList.appendList(PHDLibraries.captureAccel())
        baseLineDistAve=baseLineDistList.average()
        state=1
    
    if (state==1):
        if (x%count2==1):
            fileName="7Test"+str(x/1000)+".txt"
            file = open(fileName, 'w')
            gps=PHDLibraries.captureGPS()
            file.write(str(gps)+time.strftime("%c")+"\n")

        z=PHDLibraries.captureAccel()
        accelRunningAverage.appendList(z)
        if ((z>accelTriggerHigh)|(z<accelTriggerLow)):
            trigger=1
            #state=2
            #PHDLibraries.lcdprint('Triggered')
        else:
            trigger=0
        if (x%count1==0):
            dist=PHDLibraries.captureDistance()
            distRunningAverage.appendList(dist)
        file.write(str(x)+" "+str(z)+" "+str(dist)+" "+str(trigger)+"\n")
        if (x%count2==0):
            file.close()
        x+=1

    if (state==2):
        x+=1
        xMax=x+1000
        trigger=2
        dist=PHDLibraries.captureDistance()
        file.write(str(x)+" "+str(z)+" "+str(dist)+" "+str(trigger)+"\n")
        if ((dist<distTriggerLow)|(dist>distTriggerHigh)|(x>xMax)):
            PHDLibraries.captureCamera(name)
            state=1

    if (state==3):
        file=open(fileName, 'w')
        file.write('')
#    for x in (1,loopLimit1):
#       for y in (1,loopLimit2):
#            z[y-1]=PHDLibraries.captureAccel()
#			if ((z[y-1]>350)|(z[y-1]<250)):
#                triggered=True
#                print 'I am triggered!!!!!!!!!!!!!!!!'
#        z[x-1] = PHDLibraries.captureAccel()
#        dist[x-1]= PHDLibraries.captureDistance()

    if (trigger>=1):
        print '***loop completed, pothole detected'
    else:
        #print 'loop completed, no pothole detected'
        nothing=0
