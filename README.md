# potholeproject
Spring+Fall2017 SJSU Senior Project: Pot Hole Detector Kathy Ly, Tyler Carlberg, John Thompson, Weng Ong


This is the code repository for our Senior Project

PHDMainE.py and PHDLibraries.py utilize adafruit libararies for communication with their sensors and the LCD screen.

PHDMainE.py is the main Python script that enables the state machine for the capture of data while driving

Flask.py customizes the Flask microframework for our website hosted by DuckDNS: potholeproject.duckdns.org/8000
  this file also imports the GoogleFlaskAPI library to implement Google Map API's on the website

htmlcode.html is the html code file to provide basic formating for the website

PHDboot.sh is a script ran on the RaspberryPi on boot, calling PHDmainE.py and sending the files written before shutting down

update_main.sh is the crontad script used to reupdate the data files on the server

#add sh scripts for rpi and aws
