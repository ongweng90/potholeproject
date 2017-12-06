#!/bin/bash

# /etc/init.d/PHDboot.sh
### BEGIN INIT INFO
# Provides: PHDboot.sh
# Required-Start: $all
# Required-Stop $all
# Default-Start 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Boot script for PHD
# Description: PHD script to call main scripts and handles file transfer, shuts down at the end
### END INIT INFO

echo "begin script"
echo "running main script"
/usr/bin/python2.7 /home/pi/DistanceDetector/PHDMainE.py
#/usr/bin/python2.7 /home/pi/DistanceDetector/test_k_const.py

echo "sending files to server"
scp /home/pi/DistanceDetector/pic* ec2-user@ec2-54-153-33-174.us-west-1.compute.amazonaws.com:/home/ec2-user/static/images/
scp /home/pi/DistanceDetector/trigger* ec2-user@ec2-54-153-33-174.us-west-1.compute.amazonaws.com:/home/ec2-user/
scp /home/pi/DistanceDetector/rough* ec2-user@ec2-54-153-33-174.us-west-1.compute.amazonaws.com:/home/ec2-user/

archivepath="/home/pi/DistanceDetector/Sent_`date +%F`"
mkdir $archivepath

echo "moving files to $archivepath"
mv /home/pi/DistanceDetector/pic* $archivepath
mv /home/pi/DistanceDetector/trigger* $archivepath
mv /home/pi/DistanceDetector/rough* $archivepath

#echo "end script; waiting 60s; shutting down"
#sleep 60
#echo "shutting down"
#sudo -S poweroff

#configured /etc/lightdm/lightdm.conf for autologin into user pi and run this script
