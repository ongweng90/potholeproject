#!/usr/bin/python2.7

import argparse
import PHDLibraries

#takes a string argument and utilizing PHDLibraries send characters to LCD

parser = argparse.ArgumentParser(description="enter text to show")
parser.add_argument("-t","--text", help="text to show")
args= parser.parse_args()
if args.text:
    msg = args.text

PHDLibraries.lcdprint(msg)