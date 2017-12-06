#!/bin/bash

#gets the length of the string for the current path. This helps
#parse file names
pathLength=${#char}
let "pathLength +=1"
#echo $pathLength

#Moves all files that start with pic to Files directory
for f in "$PWD"/*;
do 
if [ "${f:$pathLength:3}" = "pic" ];
then
#echo "${f:$pathLength}"
#cp $f "$PWD"/Files
fi;
done
#if [ ! -d "$PWD"/Files ]; then
#echo $PWD
#fi

#this part makes sure the Files subdirectory exists
if [ -d "$PWD"/Files ]; 
then
#echo "Files subdirectory found"
else
#echo "not found"
mkdir "$PWD"/Files
fi

#cp "$PWD"/file* "$PWD"/Files/


#index="hello"
#for i in '"$PWD"/index.txt'; do echo $((1+$i)) ;done # echo i+1 >> "$PWD"/index.txt

#python ./testpy.py -p "$PWD"/ -f file_name
