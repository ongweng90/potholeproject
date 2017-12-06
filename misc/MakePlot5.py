import argparse
import numpy as np
import matplotlib.pyplot as plt

counter=[]
zaccel=[]
distance=[]
trigger=[]

path="5Test0.txt" #<<<<<<<<<
max = -1 #dunno how long array is
min = 0

parser = argparse.ArgumentParser(description="enter file name and range")
parser.add_argument("-f","--file", help="file name to read")
parser.add_argument("-r","--range", help="two ints: start space", type=int,
                    nargs=2, default = [min,max])
parser.add_argument("-p","--pic", help="file name of picture",default="testpic000.png")
args= parser.parse_args()
if args.file:
    path = args.file

print("checking file: "+path+"...") 

print("start parse...")
with open(path,'r') as f:
    str1=f.readline()
    print str1
str2=str1.split()
n=[]
count=1
counter.append(0)
for i in range(len(str2)):
    print str2[i]
    if count==1:
        zaccel.append(int(str2[i]))
    if count==2:
        distance.append(int(str2[i]))
    if count==3:
        trigger.append(int(str2[i][0])) 
    count+=1
    if count>3:
        counter.append(i*10)
        count=1
    

for line in n:
        numbers=line.split()
        counter.append(int(numbers[0]))
        zaccel.append(int(numbers[1]))
        distance.append(int(numbers[2]))
        trigger.append(int(numbers[3]))
        #print numbers
print("done parsing...."+str(len(counter))+" items")

#boundary checking
max=len(counter)-1

#dist2
dl_filter_max=3
dl2_counter=0
dl2_check=0
dl2_noise_tolerance=5
tempd=distance[0]
###
dl2=[]

#for iter in range(0,len(counter)):
#   if dl2_counter==0:
#      dl2_check=distance[iter]
#     dl2_counter+=1
    
#    if dl2_counter!=0:
#        if abs(dl2_check-distance[iter])>dl2_noise_tolerance:
#            dl2_counter=0
#        else:
#            dl2_counter+=1

#    if dl2_counter==dl_filter_max:
#        tempd=int(dl2_check)
#        dl2_counter=0
        
#    dl2.append(tempd)
#print dl2
###

lstart = args.range[0]
print(str(lstart))
if lstart<min or lstart>max:
    lstart=min

lstop = args.range[1]
print(str(lstop))

if lstop>max or lstop<=lstart:
    lstop=max

print ("read list lengths:"+str(lstart)+" to "+str(lstop))

c1=counter[lstart:lstop]
counter2=[x-lstart for x in c1]
z1=zaccel[lstart:lstop]
newzl=[x/304.0 for x in z1]
d1=distance[lstart:lstop]
newd1=[x/1000.0 for x in d1]
t1=trigger[lstart:lstop]
d2=dl2[lstart:lstop]

plt.figure(figsize=(8,10))
plt.figure(1)


plt.subplot(311)
plt.plot(counter2,newzl)

plt.title("Accelerometer and Distance Sensor Data")
plt.ylabel("Raw Accel. (g)")
print("done subplot1....")

plt.subplot(312)
plt.plot(counter2,newd1)
plt.ylabel("Raw Dist. Intensity")
print("done subplot2....")

plt.subplot(313)
plt.plot(counter2,t1)
plt.ylabel("Trigger Flag")
print("done subplot3....")

#plt.subplot(414)
#plt.plot(c1,d2)
#plt.ylabel("Filtered Dist.")
plt.xlabel("Data Sample (200 samples/s)")
plt.tight_layout()

print("done subplot4....")

picname=args.pic
plt.savefig(picname)

print("done saving fig "+picname+" end.")