# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
from azure.cli.core.commands import CliCommandType
from azext_vmware_cs._client_factory import (cf_vmware_cs,
                                             cf_virtual_machine,
                                             cf_private_cloud_by_region)
from ._utils import get_vmware_provider
from ._config import VmwareProviders


def load_command_table(self, _):

    custom_tmpl = 'azext_vmware_cs.custom#{}'
    custom_type = CliCommandType(operations_tmpl=custom_tmpl)

    with self.command_group('vmware', is_preview=True) as g:
        g.custom_command('set-provider', 'set_provider')
        g.custom_command('get-provider', 'get_provider')

    if get_vmware_provider() == VmwareProviders.CS:

        with self.command_group('vmware vm', client_factory=cf_virtual_machine) as g:
            g.custom_command('create', 'create_vmware_cs_vm')
            g.custom_command('add-disk', 'add_vmware_cs_vdisk')
            g.custom_command('add-nic', 'add_vmware_cs_vnic')
            g.custom_command('delete', 'delete_vmware_cs_vm')
            g.custom_command('list', 'list_vmware_cs_vm')
            g.custom_command('show', 'get_vmware_cs_vm')
            g.custom_command('start', 'start_vmware_cs_vm')
            g.custom_command('stop', 'stop_vmware_cs_vm')
            g.generic_update_command('update', getter_name='get_vmware_cs_vm', setter_name='update_vmware_cs_vm',
                                     command_type=custom_type, supports_no_wait=True)

        with self.command_group('vmware vm', client_factory=cf_vmware_cs) as g:
            g.custom_command('list-template', 'list_vm_template_by_PC')

        with self.command_group('vmware', client_factory=cf_vmware_cs) as g:
            g.custom_command('list-virtual-networks', 'list_virtual_networks')
            g.custom_command('set-region', 'set_region')
            g.custom_command('get-region', 'get_region')
            g.custom_command('list-resource-pool', 'list_resource_pool_by_PC')

        with self.command_group('vmware', client_factory=cf_private_cloud_by_region) as g:
            g.custom_command('list-private-cloud', 'list_private_cloud_by_region')

        with self.command_group('vmware', is_preview=True):
            pass
