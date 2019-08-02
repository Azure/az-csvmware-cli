# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps  # pylint: disable=unused-import
from ._utils import get_vmware_provider
from ._config import VmwareProviders

helps['vmware'] = """
    type: group
    short-summary: Commands to manage Azure VMware Solution. To see a provider's commands, you have to set the provider using set-provider command.
"""

helps['vmware set-provider'] = """
    type: group
    short-summary: Set the Azure VMware Solution provider.
"""

helps['vmware get-provider'] = """
    type: group
    short-summary: Returns the Azure VMware Solution provider.
"""

if get_vmware_provider() == VmwareProviders.CS:

    helps['vmware vm'] = """
        type: group
        short-summary: Commands to manage VMware virtual machines.
    """

    helps['vmware vm create'] = """
        type: command
        short-summary: Create or update a VMware virtual machine.
    """

    helps['vmware vm add-nic'] = """
        type: command
        short-summary: Add a virtual network interface in the VMware virtual machine.
    """

    helps['vmware vm add-disk'] = """
        type: command
        short-summary: Add a virtual disk in the VMware virtual machine.
    """

    helps['vmware vm list'] = """
        type: command
        short-summary: Returns a list of VMware virtual machines in the current subscription. If resource group is specified, only the virtual machines in that resource group would be listed.
    """

    helps['vmware vm list-template'] = """
        type: command
        short-summary: Returns a list of VMware virtual machines templates in a private cloud, either by its name (or id) or in a resource pool.
    """

    helps['vmware list-virtual-networks'] = """
        type: command
        short-summary: Returns a list of available virtual networks in a private cloud, either by its name (or id) or through resource pool.
    """

    helps['vmware vm delete'] = """
        type: command
        short-summary: Delete a VMware virtual machine.
    """

    helps['vmware vm show'] = """
        type: command
        short-summary: Returns a VMware virtual machine.
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
        short-summary: Update VMware virtual machine tags.
    """

    helps['vmware list-private-cloud'] = """
        type: command
        short-summary: Returns a list of private clouds in the current region. The current region can be changed by "az vmware set-region" command.
    """

    helps['vmware set-region'] = """
        type: command
        short-summary: Set your current region.
    """

    helps['vmware get-region'] = """
        type: command
        short-summary: Returns your current set region.
    """

    helps['vmware list-resource-pool'] = """
        type: command
        short-summary: Returns a list of resource pool templates in the specified private cloud. If resource pool is specified, that resource pool would be returned.
    """
