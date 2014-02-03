#!/usr/bin/python

"""
Script to grab a bunch of apts I need.

You probably need to sudo this script
"""

import subprocess

apts = [
    "aptitude",
    "vim",
    "scons",
    "python3.3",
    "git",
    "screen",
    "sl",
    ]

call = ["apt-get", "install"]

errored = []

for apt in apts:    
    print("*****************************")
    print("Installing {0}".format(apt))
    print("*****************************")
    try:
        subprocess.check_call(call + [apt])
    except Exception as e:
        errored.append(apt)

if len(errored) != 0:
    print("***************************************")
    print("The following apts failed to be gotten:")
    print(", ".join(errored))
print("***************************************")
