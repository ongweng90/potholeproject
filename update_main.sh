#!/bin/bash

#called every minute by crontab, append and move files to a Processed folder
cat trigger* >> MainTrigger.txt
cat roughness* >> MainRoughness.txt
mv trigger* /home/ec2-user/Processed/
mv roughness* /home/ec2-user/Processed/
