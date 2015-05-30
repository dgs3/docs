#!/usr/bin/env.exe python

"""
A Script to manage starting, stopping and getting the IP of
a virtual machine on windows.
"""

import argparse
import subprocess

vbox_manage = "c:/Program Files/Oracle/VirtualBox/VBoxManage.exe"

def start_vm(vm_name):
    subprocess.check_call([vbox_manage,
                           "startvm",
                           vm_name,
                           "--type", "headless"])

def poweroff(vm_name):
    subprocess.check_call([vbox_manage,
                           "controlvm",
                           vm_name,
                           "poweroff"])

def get_vm_ip(vm_name):
    print subprocess.check_output([vbox_manage,
                                   "guestproperty",
                                   "get",
                                    vm_name,
                                    "/VirtualBox/GuestInfo/Net/0/V4/IP"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")
    start_vm_parser = subparser.add_parser("start-vm",
                                    help="Start a vm")
    start_vm_parser.add_argument("vm_name",
                          default="ubuntu_1404_dev",
                          help="Name of the VM to start")
    poweroff_parser = subparser.add_parser("poweroff",
                                    help="poweroff a VM")
    poweroff_parser.add_argument("vm_name",
                          default="ubuntu_1404_dev",
                          help="Name of the VM to start")
    get_vm_ip_parser = subparser.add_parser("get-vm-ip",
                                    help="get the ip of a VM")
    get_vm_ip_parser.add_argument("vm_name",
                          default="ubuntu_1404_dev",
                          help="Name of the VM to start")
    args = parser.parse_args()
    actions = {"start-vm": start_vm,
               "poweroff": poweroff,
               "get-vm-ip": get_vm_ip,}
    actions[args.command](args.vm_name)
