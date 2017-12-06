#!/usr/bin/python2.7
#revised 11/3/2017

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
    print tempk
    k=tempk[0]**1.25+tempk[1]/100 #feel free to change this formula; hoping this gives me a value from 0-100
    k=int(k/10)
    if(k>10):
        k=10
    return k

n=[]
with open('4Test0.txt') as f:
    junk=f.readline() #get rid of date
    for line in f:
        n.append(line.split())
       
for i in range(len(n)):
    for j in range(len(n[i])):
        n[i][j]=float(n[i][j])

k=[0,0,0,0]
k[0]=findroughness_k(n) #all data
k[1]=findroughness_k(n[0:500]) #pre trigger data
k[2]=findroughness_k(n[600:]) #trigger somewhere in here
n=[] #null test
k[3]=findroughness_k(n)

print k
