#!/bin/bash
cat trigger* >> MainTrigger.txt
cat roughness* >> MainRoughness.txt
mv trigger* /home/ec2-user/Processed/
mv roughness* /home/ec2-user/Processed/
