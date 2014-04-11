#!/usr/bin/env python

"""
Script to grab a bunch of apts I need.

You probably need to sudo this script
"""

import os
import shutil
import subprocess

def setup_apts():
    apts = [
        "audacious",
        "aptitude",
        "chromium-chromedriver",
        "cmatrix",
        "graphviz",
        "mosh",
        "vim",
        "scons",
        "python3.3",
        "git",
        "sl",
        "tmux",
        "ispell",
        "xclip",
        "postgresql-client",
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
        shutil.copy2(f, os.path.join(os.environ["HOME"], ".{0}".format(path)))

    with open(os.path.join(base_path, "bashrc")) as my_bashrc:
        with open(os.path.join(os.environ["HOME"], ".{0}".format("bashrc")), "ab") as host_bashrc:
            host_bashrc.write(my_bashrc.read())

def setup_mosh():
    print("***************************")
    print("Setting up mosh ssh replacement")
    print("***************************")
    script = "setup_mosh.sh"
    try:
        subprocess.check_call(["./setup_mosh.sh"])
    except subprocess.CalledProcessError as e:
        print("***************************")
        print("Failed to setup mosh...")
        print("***************************")
    else:
        print("***************************")
        print("Successfully setup mosh")
        print("***************************")

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
    parser.add_argument(
        "--mosh",
        dest="mosh",
        action="store_true",
        default=False,
        help="Setup the mosh ssh replacement")
    args = parser.parse_args()
    mapping = {
        "git": setup_git,
        "apts": setup_apts,
        "configs": setup_configs,
        "mosh": setup_mosh,
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
