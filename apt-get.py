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
print("***************************************\n\n")

print("***************************************")
print("Setting Up Git")
print("***************************************")
git_config_call = ["git", "config", "--global"]
failed = []
for call in [
             ["user.name", "dgs3"], 
             ["user.email", "sayles.dave@gmail.com"],
             ["core.editor", "vi"],
            ]:
    try:
        print("Setting {0}".format(" ".join(call)))
        subprocess.check_call(git_config_call + call)
    except Exception as e:
        failed.append(call)
if len(failed) != 0:
    for call in failed:
        print("Failed to execute {0}".format(" ".join(call)))
