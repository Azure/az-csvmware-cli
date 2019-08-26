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
"""

helps['vmware get-provider'] = """
    type: command
    short-summary: Get the Azure VMware Solution provider.
"""

if get_vmware_provider() == VmwareProviders.CS:

    helps['vmware vm'] = """
        type: group
        short-summary: Manage VMware virtual machines.
    """

    helps['vmware vm create'] = """
        type: command
        short-summary: Create or update a VMware virtual machine.
    """

    helps['vmware vm add-nic'] = """
        type: command
        short-summary: Add virtual network interface to a VMware virtual machine.
    """

    helps['vmware vm add-disk'] = """
        type: command
        short-summary: Add virtual disk to a VMware virtual machine.
    """

    helps['vmware vm list'] = """
        type: command
        short-summary: Get the list of VMware virtual machines in the current subscription. If resource group is specified, only the virtual machines in that resource group would be listed.
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
        short-summary: Get the list of VMware virtual machines templates in a private cloud, either by its name (or id) or in a resource pool.
                       If resource pool is specified, the VM templates in that resource group would be listed.
                       If name of the VM template is specified, it's details would be returned.
    """

    helps['vmware virtual-network'] = """
        type: group
        short-summary: Manage virtual networks.
    """

    helps['vmware virtual-network list'] = """
        type: command
        short-summary: Get the list of available virtual networks in a private cloud, either by its name (or id) or in a resource pool.
                       If resource pool is specified, the virtual networks in that resource group would be listed.
                       If name of the virtual network is specified, it's details would be returned.
    """

    helps['vmware private-cloud'] = """
        type: group
        short-summary: Manage VMware private clouds.
    """

    helps['vmware private-cloud list'] = """
        type: command
        short-summary: Get the list of private clouds in the current region. The current region can be changed by "az vmware set-region" command.
    """

    helps['vmware resource-pool'] = """
        type: group
        short-summary: Manage VMware resource pools.
    """

    helps['vmware resource-pool list'] = """
        type: command
        short-summary: Get the list of resource pool templates in the specified private cloud. If name of the resource pool is specified, it's details would be returned.
    """
