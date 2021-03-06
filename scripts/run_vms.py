#!/usr/bin/env python

"""
Script to easily create installable storage volumes
"""

from __future__ import print_function

import argparse
import subprocess

def call_cmd(call):
    """Call subprocess command"""
    print("Calling {}".format(" ".join(call)))
    subprocess.check_call(call)

def parse_args():
    """Parse args"""
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers()
    install_vm_sub = subparsers.add_parser('run-installable-vms',
                                           help='Create VM to install')
    install_vm_sub.add_argument('--storage-name',
                                help='Name of image to install to.  This '
                                     'image is saved as a .qcow2 image')
    install_vm_sub.add_argument('--vm-name',
                                help='Name of the VM to run')
    install_vm_sub.set_defaults(func=installable_vms)
    run_vm_sub = subparsers.add_parser('run-vm',
                                       help='Just run the VM')
    run_vm_sub.add_argument('--vm-name',
                            help='VM to run')
    run_vm_sub.add_argument('--tap-interface',
                            help='Number of the tap interface to use')
    run_vm_sub.set_defaults(func=run_vm)
    return parser.parse_args()

def create_vm_storage(storage_name):
    """Cretae a VM storage file to install cloudready to"""
    call = ["qemu-img", "create", "-f", "qcow2", storage_name, "24G"]
    call_cmd(call)

def installable_vms(args):
    """Launches a VM with attached storage volume for installation"""
    storage_name = args.storage_name
    storage_size = '24G'
    create_storage_call = ['qemu-img',
                           'create', '-f', 'qcow2', storage_name, storage_size]
    call_cmd(create_storage_call)

    vm_name = args.vm_name
    call = ["qemu-system-x86_64",
            "-enable-kvm",
            "-m", "4G",
            "-smp", "4",
            "-boot", "menu=on,splash-time=30000",
            "-cpu", "core2duo",
            "-vga", "cirrus",
            "-vnc", "*:1",
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

def run_vm(args):
    """Launch storage volume"""
    vm_name = args.vm_name
    if args.tap_interface:
        # this increments the mac addr so we don't overlap
        mac = '52:54:00:12:34:5{}'.format(6+int(args.tap_interface))
        tap = "tap,id=network{},ifname=tap{},script=no,downscript=no"
        tap = tap.format(args.tap_interface, args.tap_interface)
        device = "e1000,netdev=network{},mac={}"
        device = device.format(args.tap_interface, mac)
        vnc = '*:{}'.format(args.tap_interface)
        net_args = [
            "-netdev", tap,
            "-device", device,
            "-vnc", vnc
        ]
    else:
        net_args = [
            "-net", "nic,model=virtio,macaddr=52:54:00:12:34:56",
            "-net", "user,hostfwd=tcp::9222-:22",
            "-vnc", "*:1",
        ]
    call = ["/home/dgs3/data/qemu/x86_64-softmmu/qemu-system-x86_64",
            "-enable-kvm",
            "-m", "8G",
            "-smp", "8",
            "-cpu", "SandyBridge,-invpcid,-tsc-deadline,check",
            "-vga", "cirrus",
            "-hda", vm_name]
    call += net_args
    call_cmd(call)

def main():
    """Main"""
    args = parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
