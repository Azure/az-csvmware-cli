# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long
"""
This file manages the arguments for all the commands. Names, help strings, types, validation, etc of argument is done over here.
"""

from azure.cli.core.commands.parameters import (resource_group_name_type,
                                                get_location_type,
                                                get_resource_name_completion_list,
                                                tags_type,
                                                get_enum_type,
                                                get_three_state_flag)
from azext_vmware_cs.vendored_sdks.models.vmware_cloud_simple_client_enums import (StopMode,
                                                                                   NICType,
                                                                                   DiskIndependenceMode)
from ._validators import (private_cloud_name_or_id_validator,
                          template_name_or_id_validator,
                          resource_pool_name_or_id_validator,
                          ram_validator, cores_validator,
                          disk_size_validator,
                          private_cloud_only_name_validator,
                          resource_pool_only_name_validator,
                          template_only_name_validator,
                          vnet_only_name_validator,
                          vm_name_validator,
                          location_validator)
from ._utils import get_vmware_provider
from ._actions import (AddNicAction, AddDiskAction)
from ._config import VmwareProviders


def load_arguments(self, _):
    """
    Load argument method of command loader.
    """

    with self.argument_context('vmware') as c:
        c.argument('provider_name', options_list=['--name', '-n'],
                   help="Name of the Azure VMware Service provider.",
                   arg_type=get_enum_type(VmwareProviders))

    if get_vmware_provider() == VmwareProviders.CS:

        with self.argument_context('vmware') as c:
            c.argument('resource_group_name', arg_type=resource_group_name_type)
            c.argument('tags', arg_type=tags_type)
            c.argument('region_name', options_list=['--name', '-n'],
                       help="Location of your Azure resource.")

        with self.argument_context('vmware vm') as c:
            c.argument('location', get_location_type(self.cli_ctx), validator=location_validator,
                       help="Location in which to create VM. If default location is not configured, will default to the resource group\'s location")
            c.argument('vm_name', options_list=['--name', '-n'],
                       help="Name of the virtual machine.",
                       validator=vm_name_validator,
                       completer=get_resource_name_completion_list('Microsoft.VMwareCloudSimple/virtualMachines'))
            c.argument('amount_of_ram', options_list=['--ram'],
                       validator=ram_validator,
                       help="The amount of memory in MB. The default is taken from the vSphere VM template specified.")
            c.argument('stop_mode', options_list=['--mode'], arg_type=get_enum_type(StopMode),
                       help="Stop mode.")
            c.argument('number_of_cores', options_list=['--cores'],
                       validator=cores_validator,
                       help="The number of CPU cores required. The default is taken from the vSphere VM template specified.")
            c.argument('resource_pool', options_list=['--resource-pool', '-r'],
                       validator=resource_pool_name_or_id_validator,
                       completer=get_resource_name_completion_list('Microsoft.VMwareCloudSimple/resourcePools'),
                       help="Name or ID of the VMware resource pool for this virtual machine in your CloudSimple Private Cloud.")
            c.argument('template', options_list=['--template'],
                       validator=template_name_or_id_validator,
                       completer=get_resource_name_completion_list('Microsoft.VMwareCloudSimple/virtualmachinetemplates'),
                       help="Name or ID of the vSphere template from which this virtual machine will be created.")
            c.argument('private_cloud', options_list=['--private-cloud', '-p'],
                       validator=private_cloud_name_or_id_validator,
                       completer=get_resource_name_completion_list('Microsoft.VMwareCloudSimple/privateClouds'),
                       help="Name or ID of the CloudSimple private cloud.")
            c.argument('expose_to_guest_vm', options_list=['--expose-to-guest-vm'],
                       arg_type=get_three_state_flag(),
                       help="Will expose full CPU virtualization to the guest operating system. The default is taken from the vSphere VM template specified.")

            c.argument('nics', options_list=['--nic'], action=AddNicAction, arg_group='Network', nargs='+')

            c.argument('disks', options_list=['--disk'], action=AddDiskAction, arg_group='Storage', nargs='+')

            c.argument('controller', options_list=['--controller'], arg_group='Storage',
                       help="The SCSI controller.")
            c.argument('independence_mode', options_list=['--mode'], arg_group='Storage',
                       arg_type=get_enum_type(DiskIndependenceMode),
                       help="The disk independence mode.")
            c.argument('size', options_list=['--size'], arg_group='Storage',
                       validator=disk_size_validator,
                       help="The amount of disk size in KB.")
            c.argument('disk_name', options_list=['--name', '-n'], arg_group='Storage',
                       help="Name of the disk.")

        with self.argument_context('vmware vm nic') as c:
            c.argument('vm_name', options_list=['--vm-name'],
                       help="Name of the virtual machine.",
                       validator=vm_name_validator,
                       completer=get_resource_name_completion_list('Microsoft.VMwareCloudSimple/virtualMachines'))
            c.argument('virtual_network', options_list=['--virtual-network'],
                       help="Name or ID of the virtual network.")
            c.argument('adapter', options_list=['--adapter'],
                       arg_type=get_enum_type(NICType),
                       help="The adapter for the NIC.")
            c.argument('power_on_boot', options_list=['--power-on-boot'],
                       arg_type=get_three_state_flag(),
                       help="Will power on the NIC at boot time.")
            c.argument('nic_name', options_list=['--name', '-n'],
                       help="Name of the NIC.")
            c.argument('nic_names', options_list=['--nics'], nargs='+',
                       help="Names of NICs.")

        with self.argument_context('vmware vm disk') as c:
            c.argument('vm_name', options_list=['--vm-name'],
                       help="Name of the virtual machine.",
                       validator=vm_name_validator,
                       completer=get_resource_name_completion_list('Microsoft.VMwareCloudSimple/virtualMachines'))
            c.argument('controller', options_list=['--controller'],
                       help="The SCSI controller.")
            c.argument('independence_mode', options_list=['--mode'],
                       arg_type=get_enum_type(DiskIndependenceMode),
                       help="The disk independence mode.")
            c.argument('size', options_list=['--size'],
                       validator=disk_size_validator,
                       help="The amount of disk size in KB.")
            c.argument('disk_name', options_list=['--name', '-n'],
                       help="Name of the disk.")
            c.argument('disk_names', options_list=['--disks'], nargs='+',
                       help="Names of disks.")

        with self.argument_context('vmware vm-template') as c:
            c.argument('private_cloud', options_list=['--private-cloud', '-p'],
                       validator=private_cloud_only_name_validator,
                       completer=get_resource_name_completion_list('Microsoft.VMwareCloudSimple/privateClouds'),
                       help="Name or ID of the CloudSimple private cloud.")
            c.argument('resource_pool', options_list=['--resource-pool', '-r'],
                       validator=resource_pool_only_name_validator,
                       completer=get_resource_name_completion_list('Microsoft.VMwareCloudSimple/resourcePools'),
                       help="Name or ID of the VMware resource pool in your CloudSimple Private Cloud.")
            c.argument('template', options_list=['--name', '-n'],
                       validator=template_only_name_validator,
                       completer=get_resource_name_completion_list('Microsoft.VMwareCloudSimple/virtualmachinetemplates'),
                       help="Name or ID of the vSphere virtual machine template.")

        with self.argument_context('vmware virtual-network') as c:
            c.argument('private_cloud', options_list=['--private-cloud', '-p'],
                       validator=private_cloud_only_name_validator,
                       completer=get_resource_name_completion_list('Microsoft.VMwareCloudSimple/privateClouds'),
                       help="Name or ID of the CloudSimple private cloud.")
            c.argument('resource_pool', options_list=['--resource-pool', '-r'],
                       validator=resource_pool_only_name_validator,
                       completer=get_resource_name_completion_list('Microsoft.VMwareCloudSimple/resourcePools'),
                       help="Name or ID of the resource pool used to derive vSphere cluster which contains virtual networks.")
            c.argument('virtual_network', options_list=['--name', '-n'],
                       validator=vnet_only_name_validator,
                       help="Name or ID of the virtual network (vsphereId).")

        with self.argument_context('vmware resource-pool') as c:
            c.argument('private_cloud', options_list=['--private-cloud', '-p'],
                       validator=private_cloud_only_name_validator,
                       completer=get_resource_name_completion_list('Microsoft.VMwareCloudSimple/privateClouds'),
                       help="Name or ID of the CloudSimple private cloud.")
            c.argument('resource_pool', options_list=['--name', '-n'],
                       validator=resource_pool_only_name_validator,
                       completer=get_resource_name_completion_list('Microsoft.VMwareCloudSimple/resourcePools'),
                       help="Name or ID of the VMware resource pool in your CloudSimple Private Cloud.")
