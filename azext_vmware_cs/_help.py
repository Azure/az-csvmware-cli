# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
This file contains the help strings (summaries) for all commands and command groups.
"""

from knack.help_files import helps  # pylint: disable=unused-import
from ._utils import get_vmware_provider
from ._config import VmwareProviders

helps['vmware'] = """
    type: group
    short-summary: Manage Azure VMware Solution. To see a provider's commands, you have to set the provider using set-provider command.
"""

helps['vmware set-provider'] = """
    type: command
    short-summary: Set the Azure VMware Solution provider.
    examples:
        - name: Set provider to cs
          text: >
            az vmware set-provider -n cs
        - name: Set provider to vs
          text: >
            az vmware set-provider -n vs
"""

helps['vmware get-provider'] = """
    type: command
    short-summary: Get the Azure VMware Solution provider.
    examples:
        - name: Get provider
          text: >
            az vmware get-provider
"""

if get_vmware_provider() == VmwareProviders.CS:

    helps['vmware vm'] = """
        type: group
        short-summary: Manage VMware virtual machines.
    """

    helps['vmware vm create'] = """
        type: command
        short-summary: Create a VMware virtual machine.

        parameters:
            - name: --nic
              short-summary: Add or modify NICs.
              long-summary: |
                By default, the nics will be added according to the vSphere VM template.
                You can add more nics, or modify some properties of a nic specified in the VM template.
                Multiple nics can be specified by using more than one `--nic` argument.
                If a nic name already exists in the VM template, that nic would be modified according to the user input.
                If a nic name does not exist in the VM template, a new nic would be created and a new name will be assigned to it.
                Usage:   --nic name=MyNicName virtual-network=MyNetwork adapter=MyAdapter power-on-boot=True/False

            - name: --disk
              short-summary: Add or modify disks.
              long-summary: |
                By default, the disks will be added according to the vSphere VM template.
                You can add more disks, or modify some properties of a disk specified in the VM template.
                Multiple disks can be specified by using more than one `--disk` argument.
                If a disk name already exists in the VM template, that disk would be modified according to the user input.
                If a disk name does not exist in the VM template, a new disk would be created and a new name will be assigned to it.
                Usage:   --disk name=MyDiskName controller=SCSIControllerID mode=IndependenceMode size=DiskSizeInKB

        examples:
            - name: Creating a virtual machine with default parameters from the vm template.
              text: >
                az vmware vm create -n MyVm -g MyResourceGroup -p MyPrivateCloud -r MyResourcePool --template MyVmTemplate

            - name: Creating a virtual machine and adding an extra nic to the VM with virtual network MyVirtualNetwork, adapter VMXNET3, that power ups on boot.
                    The name entered in the nic is for identification purposes only, to see if such a nic name exists in the vm template, else a nic is created and name is reassigned.
                    Lets say the vm template contains a nic with name "Network adapter 1".
              text: >
                az vmware vm create -n MyVm -g MyResourceGroup -p MyPrivateCloud -r MyResourcePool --template MyVmTemplate --nic name=NicNameWouldBeReassigned virtual-network=MyVirtualNetwork adapter=VMXNET3 power-on-boot=True

            - name: Customizing specific properties of a VM. Changing the number of cores to 2 and adapter of "Network adapter 1" nic to E1000E, from that specified in the template. All other properties would be defaulted from the template.
              text: >
                az vmware vm create -n MyVm -g MyResourceGroup -p MyPrivateCloud -r MyResourcePool --template MyVmTemplate --cores 2 --nic name="Network adapter 1" adapter=E1000E

            - name: Customizing specific properties of a VM. Changing the adapter of "Network adapter 1" nic to E1000E, from that specified in the template, and also adding another nic with virtual network MyVirtualNetwork, adapter VMXNET3, that power ups on boot.
              text: >
                az vmware vm create -n MyVm -g MyResourceGroup -p MyPrivateCloud -r MyResourcePool --template MyVmTemplate --nic name="Network adapter 1" adapter=E1000E --nic name=NicNameWouldBeReassigned virtual-network=MyVirtualNetwork adapter=VMXNET3 power-on-boot=True

            - name: Creating a virtual machine and adding an extra disk to the VM with SCSI controller 0, persistent mode, and 41943040 KB size.
                    The name entered in the disk is for identification purposes only, to see if such a disk name exists in the vm template, else a disk is created and name is reassigned.
                    Lets say the vm template contains a disk with name "Hard disk 1".
              text: >
                az vmware vm create -n MyVm -g MyResourceGroup -p MyPrivateCloud -r MyResourcePool --template MyVmTemplate --disk name=DiskNameWouldBeReassigned controller=1000 mode=persistent size=41943040

            - name: Customizing specific properties of a VM. Changing the size of "Hard disk 1" disk to 21943040 KB, from that specified in the template, and also adding another disk with SCSI controller 0, persistent mode, and 41943040 KB size.
              text: >
                az vmware vm create -n MyVm -g MyResourceGroup -p MyPrivateCloud -r MyResourcePool --template MyVmTemplate --disk name="Hard disk 1" size=21943040 --disk name=DiskNameWouldBeReassigned controller=1000 mode=persistent size=41943040
    """

    helps['vmware vm list'] = """
        type: command
        short-summary: List details of VMware virtual machines in the current subscription. If resource group is specified, only the details of virtual machines in that resource group would be listed.
    """

    helps['vmware vm delete'] = """
        type: command
        short-summary: Delete a VMware virtual machine.
    """

    helps['vmware vm show'] = """
        type: command
        short-summary: Get the details of a VMware virtual machine.
    """

    helps['vmware vm start'] = """
        type: command
        short-summary: Start a VMware virtual machine.
    """

    helps['vmware vm stop'] = """
        type: command
        short-summary: Stop a VMware virtual machine.
    """

    helps['vmware vm update'] = """
        type: command
        short-summary: Update the tags field of a VMware virtual machine.
    """

    helps['vmware vm nic'] = """
        type: group
        short-summary: Manage VMware virtual machine's Network Interface Cards.
    """

    helps['vmware vm nic add'] = """
        type: command
        short-summary: Add NIC to a VMware virtual machine.
    """

    helps['vmware vm nic list'] = """
        type: command
        short-summary: List details of NICs available on a VMware virtual machine.
    """

    helps['vmware vm nic show'] = """
        type: command
        short-summary: Get the details of a VMware virtual machine's NIC.
    """

    helps['vmware vm nic delete'] = """
        type: command
        short-summary: Delete NICs from a VM.
    """

    helps['vmware vm disk'] = """
        type: group
        short-summary: Manage VMware virtual machine's disks.
    """

    helps['vmware vm disk add'] = """
        type: command
        short-summary: Add disk to a VMware virtual machine.
    """

    helps['vmware vm disk list'] = """
        type: command
        short-summary: List details of disks available on a VMware virtual machine.
    """

    helps['vmware vm disk show'] = """
        type: command
        short-summary: Get the details of a VMware virtual machine's disk.
    """

    helps['vmware vm disk delete'] = """
        type: command
        short-summary: Delete disks from a VM.
    """

    helps['vmware set-region'] = """
        type: command
        short-summary: Set the current region.
    """

    helps['vmware get-region'] = """
        type: command
        short-summary: Get the current region.
    """

    helps['vmware vm-template'] = """
        type: group
        short-summary: Manage VMware virtual machine templates.
    """

    helps['vmware vm-template list'] = """
        type: command
        short-summary: List details of VMware virtual machines templates in a resource pool, in a private cloud.
    """

    helps['vmware vm-template show'] = """
        type: command
        short-summary: Get the details of a VMware virtual machines template in a private cloud.
    """

    helps['vmware virtual-network'] = """
        type: group
        short-summary: Manage virtual networks.
    """

    helps['vmware virtual-network list'] = """
        type: command
        short-summary: List details of available virtual networks in a resource pool, in a private cloud.
    """

    helps['vmware virtual-network show'] = """
        type: command
        short-summary: Get the details of a virtual network in a private cloud.
    """

    helps['vmware private-cloud'] = """
        type: group
        short-summary: Manage VMware private clouds.
    """

    helps['vmware private-cloud list'] = """
        type: command
        short-summary: List details of private clouds in the current region. The current region can be changed by "az vmware set-region" command.
    """

    helps['vmware resource-pool'] = """
        type: group
        short-summary: Manage VMware resource pool.
    """

    helps['vmware resource-pool list'] = """
        type: command
        short-summary: List details of resource pools in a private cloud.
    """

    helps['vmware resource-pool show'] = """
        type: command
        short-summary: Get the details of a resource pool in a private cloud.
    """
