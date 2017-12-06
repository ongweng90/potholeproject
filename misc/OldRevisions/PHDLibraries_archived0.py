#!/usr/bin/python2.7

#last revised 11/3/2017
import numpy
import math
import time
import picamera
import Adafruit_CharLCD as LCD

# Import the ADS1x15 module.
import Adafruit_ADS1x15
import Adafruit_ADXL345
import gps

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()
accel = Adafruit_ADXL345.ADXL345()

#Camera
camera=picamera.PiCamera()
camera.brightness = 60

#GPS
testgps=gps.gps("localhost","2947")
testgps.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

#ADC stuff
GAIN = 1
adc.start_adc(0, gain=GAIN)

# Raspberry Pi pin configuration:
lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 22
lcd_d6        = 27
lcd_d7        = 17
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)


class runningAverage(object):
    index=0
    listLength=10
    list= [0]*1
    def __init__(self, LL):
        self.listLength=LL
        self.index=0
        self.list=[0]*self.listLength

    def appendList(self, input):
        self.list[self.index]=input
        if (self.index<self.listLength-1):
            self.index+=1
        else:
            self.index=0

    def average(self):
        total=0
#      print ("self.listLength = %i" % (self.listLength))
        for x in range(0, (self.listLength)):
            total+=self.list[x]
#         print ("x is %i" % (x))
        total = float(total)/float(self.listLength)
        return total

    def deviation(self):
        average=self.average()
        numerator=0
        for x in range(0, (self.listLength)):
            numerator+=(self.list[x]-average)*(self.list[x]-average)
        denominator= float(self.listLength-1)
        deviation=float(numerator)/denominator
        deviation=math.sqrt(deviation)
        return deviation

    def printValues(self):
        print 'Values in runnning average object'
        print self.list
        average = self.average()
        deviation= self.deviation()
        print ('index = %i , average = %d ,  deviation = %d' % (self.index,  average, deviation))

class flat_filter(object):
    dl_filter_max=3
    dl2_counter=0
    dl2_check=0
    dl2_noise_tolerance=5
    dl2=0

    def __init__(self):
        self.dl_filter_max=4
        self.dl2_counter=0
        self.dl2_check=0
        self.dl2_noise_tolerance=5
        self.dl2=0
    
    def filter_dl(self,dl):
        if self.dl2_counter==0:
            self.dl2_check=dl
            self.dl2_counter+=1
    
        if self.dl2_counter!=0:
            if abs(self.dl2_check-dl)>self.dl2_noise_tolerance:
                self.dl2_counter=0
            else:
                self.dl2_counter+=1

        if self.dl2_counter==self.dl_filter_max:
            self.dl2=self.dl2_check
            self.dl2_counter=0
        return self.dl2
        
#This function returns the accelerometer's z axis measurement
def captureAccel():
   x, y, z = accel.read()
   return z


#this function returns 1 if input is above threshold
def accelTrigger(input):
   highThreshold=370
   lowThreshold=250
   if (input>highThreshold):
      return 1
   elif (input<lowThreshold):
      return -1
   return 0

#This function returns the ADC value for the distance sensor
def captureDistance():
    value= adc.get_last_result()
    return value

#This function returns 1 if the distance reading is above the threshold
def distTrigger():
    return 0

#This function takes a picture and stores it at the location with name specified
def captureCamera(name):
    #directory =
    camera.capture(name)
    camera.brightness
    return 0

#Gets the GPS data
def captureGPS():
    try:
        report=testgps.next()
        if report['class'] == 'TPV':
            if hasattr(report, 'time'):
                #print(str(session.fix.longitude)+","+str(session.fix.latitude)+"\n")
                list = [testgps.fix.latitude, testgps.fix.longitude]
                #while list is None:    
                #    list = [testgps.fix.latitude, testgps.fix.longitude]
                return list
    except KeyError:
        pass
        #return
    except KeyboardInterrupt:
        quit()
        #return
    except StopIteration:
        session = None
        print "GPSD has terminated"
        #return


#This functions handles start up behavior
def start():
    return 0

#This functions handles parking/uploading 
def park():
    return 0

def lcdprint(message):
    lcd.clear()
    lcd.message(message)
    return

import numpy

def findroughness_k(rough_data):
    if not rough_data:
        return 0
    transpose=list(zip(*rough_data))
    rzvalues=transpose[1]
    distvalues=transpose[2]
    rzarray=numpy.array(rzvalues)
    distarray=numpy.array(distvalues)
    tempk=[numpy.std(rzarray,axis=0),numpy.std(distarray,axis=0)] #find standard deviation of z and distance
    #print tempk
    k=tempk[0]**1.25+tempk[1]/100 #feel free to change this formula; hoping this gives me a value from 0-100
    k=int(k/10)
    if(k>10):
        k=10
    return k