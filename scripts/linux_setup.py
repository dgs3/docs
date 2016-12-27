#!/usr/bin/env python

"""
Script to grab a bunch of apts I need.

You probably need to sudo this script
"""

import os
import shutil
import subprocess

def setup_apts():
    subprocess.check_call(["sudo", "apt-get", "update"])

    apts = [
        "aptitude",
        "chromium-chromedriver",
        "openssh-server",
        "vim",
        "git",
        "sl",
        "tmux",
        "ispell",
        "xclip",
        ]

    call = ["sudo", "apt-get", "install"]

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

def setup_git():
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

def setup_configs():
    print("***************************")
    print("Copying configuration files")
    print("***************************")
    base_path = os.path.join("..", "configs")
    for f in ["vimrc", "inputrc", "tmux.conf"]:
        path = os.path.join(base_path, f)
        shutil.copy2(path, os.path.join(os.environ["HOME"], ".{0}".format(f)))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--all",
        dest="all",
        action="store_true",
        default=False,
        help="Build all the things",)
    parser.add_argument(
        "--git",
        dest="git",
        action="store_true",
        default=False,
        help="Setup git configs",)
    parser.add_argument(
        "--apts",
        dest="apts",
        action="store_true",
        default=False,
        help="Grab all the apts via apt-get",)
    parser.add_argument(
        "--configs",
        dest="configs",
        action="store_true",
        default=False,
        help="Sets up all of the configs that go in ~/.*",)
    args = parser.parse_args()
    mapping = {
        "git": setup_git,
        "apts": setup_apts,
        "configs": setup_configs,
    }
    if getattr(args, "all", False):
        print("Building all...")
        for key, value in mapping.iteritems():
            value()
    else:
        for key, value in mapping.iteritems():
            if getattr(args, key, False):
                print("Building {0}".format(key))
                value()
