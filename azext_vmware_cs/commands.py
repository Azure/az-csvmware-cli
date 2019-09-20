# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long
"""
This file contains load_command_table method of command loader.
Here the commands are registered so that they can used in the CLI.
"""

from azure.cli.core.commands import CliCommandType
from azext_vmware_cs._client_factory import (cf_vmware_cs,
                                             cf_virtual_machine)
from ._utils import get_vmware_provider
from ._config import VmwareProviders
from ._format import (transform_vm_table_output)
from ._validators import (vm_create_namespace_validator)


def load_command_table(self, _):
    """
    Load command table method of command loader.
    """

    custom_tmpl = 'azext_vmware_cs.custom#{}'
    custom_type = CliCommandType(operations_tmpl=custom_tmpl)

    with self.command_group('vmware') as g:
        g.custom_command('set-provider', 'set_provider')
        g.custom_command('get-provider', 'get_provider')
        g.custom_command('remove-provider', 'remove_provider')

    if get_vmware_provider() == VmwareProviders.CS:

        with self.command_group('vmware vm', client_factory=cf_vmware_cs) as g:
            g.custom_command('create', 'create_vm', table_transformer=transform_vm_table_output, validator=vm_create_namespace_validator)

        with self.command_group('vmware vm', client_factory=cf_virtual_machine) as g:
            g.custom_command('list', 'list_vm', table_transformer=transform_vm_table_output)
            g.custom_command('show', 'get_vm', table_transformer=transform_vm_table_output)
            g.generic_update_command('update', getter_name='get_vm', setter_name='update_vm',
                                     command_type=custom_type, supports_no_wait=True)
            g.custom_command('delete', 'delete_vm')
            g.custom_command('start', 'start_vm')
            g.custom_command('stop', 'stop_vm')

        with self.command_group('vmware vm disk', client_factory=cf_virtual_machine) as g:
            g.custom_command('add', 'add_vdisk')
            g.custom_command('show', 'show_vdisk')
            g.custom_command('list', 'list_vdisks')
            g.custom_command('delete', 'delete_vdisks')

        with self.command_group('vmware vm nic', client_factory=cf_virtual_machine) as g:
            g.custom_command('add', 'add_vnic')
            g.custom_command('show', 'show_vnic')
            g.custom_command('list', 'list_vnics')
            g.custom_command('delete', 'delete_vnics')

        with self.command_group('vmware vm-template', client_factory=cf_vmware_cs) as g:
            g.custom_command('show', 'show_vm_template')
            g.custom_command('list', 'list_vm_template')

        with self.command_group('vmware virtual-network', client_factory=cf_vmware_cs) as g:
            g.custom_command('show', 'show_virtual_network')
            g.custom_command('list', 'list_virtual_networks')

        with self.command_group('vmware resource-pool', client_factory=cf_vmware_cs) as g:
            g.custom_command('show', 'show_resource_pool')
            g.custom_command('list', 'list_resource_pool')

        with self.command_group('vmware private-cloud', client_factory=cf_vmware_cs) as g:
            g.custom_command('list', 'list_private_cloud_by_region')
            g.custom_command('show', 'show_private_cloud')

        with self.command_group('vmware', client_factory=cf_vmware_cs) as g:
            g.custom_command('set-region', 'set_region')
            g.custom_command('get-region', 'get_region')

    with self.command_group('vmware', is_preview=True):
        pass
