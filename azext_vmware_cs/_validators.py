# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
This file contains the validation logic for arguments passed in CLI commands.
Which validator method to be used for which argument, is defined in _params.py file
"""

from knack.util import CLIError
from ._utils import (vm_cs_create_resource_id,
                     vmware_cs_name_or_id_validator,
                     only_resource_name_validator)


def _check_postive_integer(parameter, value):
    """
    Checks whether the input is a integer or not
    """
    try:
        val = int(value)
    except ValueError:
        raise CLIError(parameter + ' should be a postive integer value.')
    if val <= 0:
        raise CLIError(parameter + ' should be a postive integer value.')


def _check_regex(parameter, value):
    """
    Checks whether the input matches ^[-a-zA-Z0-9]+$ pattern
    """
    import re
    pattern = r'^[-a-zA-Z0-9]+$'
    if not re.match(pattern, value):
        raise CLIError(parameter + ' should only contain letters, numbers, or hyphen.')


def vm_name_validator(namespace):
    """
    Checks whether the vm name is following the required pattern
    """
    if namespace.vm_name:
        _check_regex('Virtual machine name', namespace.vm_name)


def ram_validator(namespace):
    """
    Checks whether the ram input is a interger or not
    """
    if namespace.amount_of_ram:
        _check_postive_integer('RAM', namespace.amount_of_ram)


def cores_validator(namespace):
    """
    Checks whether the number of cores input is a integer or not
    """
    if namespace.number_of_cores:
        _check_postive_integer('Cores', namespace.number_of_cores)


def disk_size_validator(namespace):
    """
    Checks whether the size input is a integer or not
    """
    if namespace.size:
        _check_postive_integer('Size', namespace.size)


def location_validator(cmd, namespace):
    """
    If the passed location is none, then it is defaulted to the resource group's location.
    """
    from ._client_factory import cf_resource_groups

    if not namespace.location:
        client = cf_resource_groups(cmd.cli_ctx)
        rg = client.get(namespace.resource_group_name)
        namespace.location = rg.location


def private_cloud_only_name_validator(namespace):
    """
    Checks whether the private cloud value is just the resource name (and not the resource id).
    If its the resource id, then the resource name is extracted.
    """
    if namespace.private_cloud:
        namespace.private_cloud = only_resource_name_validator(namespace.private_cloud)


def resource_pool_only_name_validator(namespace):
    """
    Checks whether the resource pool value is just the resource name (and not the resource id).
    If its the resource id, then the resource name is extracted.
    """
    if namespace.resource_pool:
        namespace.resource_pool = only_resource_name_validator(namespace.resource_pool)


def template_only_name_validator(namespace):
    """
    Checks whether the vm template value is just the resource name (and not the resource id).
    If its the resource id, then the resource name is extracted.
    """
    if namespace.template:
        namespace.template = only_resource_name_validator(namespace.template)


def vnet_only_name_validator(namespace):
    """
    Checks whether the virtual network value is just the resource name (and not the resource id).
    If its the resource id, then the resource name is extracted.
    """
    if namespace.virtual_network:
        namespace.virtual_network = only_resource_name_validator(namespace.virtual_network)


def private_cloud_name_or_id_validator(cmd, namespace):
    """
    Checks whether the private cloud value is a valid resource id.
    If not, then assuming that the passed value is a resource name, a resource id is constructed.
    If the constructed resource id is also invalid, an error is raised.
    """
    if namespace.private_cloud:
        namespace.private_cloud = vmware_cs_name_or_id_validator(cmd, namespace, 'private cloud')


def template_name_or_id_validator(cmd, namespace):
    """
    Checks whether the passed value is a valid resource id.
    If not, then assuming that the passed value is a resource name, a resource id is constructed.
    If the constructed resource id is also invalid, an error is raised.
    """
    if namespace.template:
        namespace.template = vmware_cs_name_or_id_validator(cmd, namespace,
                                                            'template',
                                                            'virtualmachinetemplates',
                                                            namespace.template)


def resource_pool_name_or_id_validator(cmd, namespace):
    """
    Checks whether the passed value is a valid resource id.
    If not, then assuming that the passed value is a resource name, a resource id is constructed.
    If the constructed resource id is also invalid, an error is raised.
    """
    if namespace.resource_pool:
        namespace.resource_pool = vmware_cs_name_or_id_validator(cmd, namespace,
                                                                 'resource pool',
                                                                 'resourcepools',
                                                                 namespace.resource_pool)


def virtual_network_name_or_id_validator(cmd, client, virtual_network, resource_group_name,
                                         vm_name, region=None, pc=None):
    """
    Checks whether the passed value is a valid resource id.
    If not, then assuming that the passed value is a resource name, a resource id is constructed.
    If the constructed resource id is also invalid, an error is raised.
    """
    from azure.cli.core.commands.client_factory import get_subscription_id
    from msrestazure.tools import is_valid_resource_id
    from ._config import PATH_CHAR

    location = region
    private_cloud = pc
    if ((pc is None) and (region is None)):
        virtual_machine = client.get(resource_group_name, vm_name)
        location = virtual_machine.location
        private_cloud = virtual_machine.private_cloud_id

    if is_valid_resource_id(private_cloud):
        private_cloud = private_cloud.rsplit(PATH_CHAR, 1)[-1]
    if not is_valid_resource_id(virtual_network):
        virtual_network = vm_cs_create_resource_id(subscription=get_subscription_id(cmd.cli_ctx),
                                                   namespace='Microsoft.VMwareCloudSimple',
                                                   location=location,
                                                   resource_type='privateClouds',
                                                   resource_name=private_cloud,
                                                   child_type='virtualnetworks',
                                                   child_name=virtual_network)
    if not is_valid_resource_id(virtual_network):
        raise CLIError('Invalid virtual network.')

    return virtual_network


def vm_create_namespace_validator(cmd, namespace):
    """
    Command validator for the create vm command.
    This calls various argument validators.
    We need this for sequencing argument validators essentially.
    More specifically we want the location validator to run before other validators,
    because some of the other argument validators requires location to be present in the namespace,
    and location validator is responsible for extracting location from resource group,
    if it is not present in namespace.
    """
    vm_name_validator(namespace)
    location_validator(cmd, namespace)
    private_cloud_name_or_id_validator(cmd, namespace)
    resource_pool_name_or_id_validator(cmd, namespace)
    template_name_or_id_validator(cmd, namespace)
    cores_validator(namespace)
    ram_validator(namespace)
