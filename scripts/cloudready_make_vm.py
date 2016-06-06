#!/usr/bin/env python

"""
Script to easily create installable storage volumes
"""

from __future__ import print_function

import argparse
import os
import subprocess

def call_cmd(call):
    """Call subprocess command"""
    print("Calling {}".format(" ".join(call)))
    subprocess.check_call(call)

def parse_args():
    """Parse args"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--storage-name")
    parser.add_argument("--vm-name")
    parser.add_argument("--create-new",
                        action="store_true")
    return parser.parse_args()

def create_vm_storage(storage_name):
    """Cretae a VM storage file to install cloudready to"""
    call = ["qemu-img", "create", "-f", "qcow2", storage_name, "24G"]
    call_cmd(call)

def launch_vm(storage_name, vm_name):
    """Launches a VM with attached storage volume for installation"""
    call = ["qemu-system-x86_64",
            "-enable-kvm",
            "-m", "4G",
            "-smp", "4",
            "-boot", "menu=on",
            "-cpu", "core2duo",
            "-vga", "cirrus",
            "-net", "nic,model=virtio,macaddr=52:54:00:12:34:56",
            "-net", "user,hostfwd=tcp::9222-:22",
            "-device", "usb-ehci",
            "-device", "virtio-scsi-pci",
            "-drive", "format=raw,if=none,id=installer,file={}".format(vm_name),
            "-drive", "if=none,id=cloudready,file={}".format(storage_name),
            "-device", "usb-storage,drive=installer,removable=yes",
            "-device", "scsi-hd,drive=cloudready"]
    print("Launching VM")
    call_cmd(call)

def launch_storage(storage_name):
    """Launch storage volume"""
    call = ["qemu-system-x86_64",
            "-enable-kvm",
            "-m", "4G",
            "-smp", "4",
            "-cpu", "core2duo",
            "-vga", "cirrus",
            "-net", "nic,model=virtio,macaddr=52:54:00:12:34:57",
            "-net", "user,hostfwd=tcp::9222-:22",
            "-hda", storage_name]
    call_cmd(call)

def main():
    """Main"""
    args = parse_args()
    storage_name = args.storage_name
    storage_ext = ".qcow2"
    if not storage_name.endswith(storage_ext):
        storage_name = storage_name + storage_ext
    if args.create_new:
        if os.path.exists(storage_name):
            raw = raw_input("Do you want to replace {} "
                            "[y/N] ".format(storage_name))
            if "y" in raw.lower():
                os.unlink(storage_name)
        create_vm_storage(storage_name)
        launch_vm(storage_name, args.vm_name)
    launch_storage(storage_name)

if __name__ == "__main__":
    main()
