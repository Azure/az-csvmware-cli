# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
This file contains the validation logic for arguments passed in CLI commands.
Which validator method to be used for which argument, is defined in _params.py file
"""

from knack.util import CLIError
from ._utils import vm_cs_create_resource_id


def _check_integer(parameter, value):
    """
    Checks whether the input is a integer or not
    """
    try:
        int(value)
        return True
    except ValueError:
        raise CLIError(parameter + ' should be an integer value.')


def ram_validator(namespace):
    """
    Checks whether the ram input is a interger or not
    """
    if namespace.amount_of_ram:
        _check_integer('Ram', namespace.amount_of_ram)


def cores_validator(namespace):
    """
    Checks whether the number of cores input is a integer or not
    """
    if namespace.number_of_cores:
        _check_integer('Cores', namespace.number_of_cores)


def disk_size_validator(namespace):
    """
    Checks whether the size input is a integer or not
    """
    if namespace.size:
        _check_integer('Size', namespace.size)


def private_cloud_name_or_id_validator(cmd, namespace):
    """
    Checks whether the passed value is a valid resource id.
    If not, then assuming that the passed value is a resource name, a resource id is constructed.
    If the constructed resource id is also invalid, an error is raised.
    """
    from azure.cli.core.commands.client_factory import get_subscription_id
    from msrestazure.tools import is_valid_resource_id
    if namespace.private_cloud:
        if not is_valid_resource_id(namespace.private_cloud):
            namespace.private_cloud = vm_cs_create_resource_id(subscription=get_subscription_id(cmd.cli_ctx),
                                                               namespace='Microsoft.VMwareCloudSimple',
                                                               location=namespace.location,
                                                               resource_type='privateClouds',
                                                               name=namespace.private_cloud)
    if not is_valid_resource_id(namespace.private_cloud):
        raise CLIError('Invalid private cloud.')


def private_cloud_only_name_validator(namespace):
    """
    Checks whether the passed value is just the resource name (and not the resource id).
    If its the resource id, then the resource name is extracted.
    """
    from msrestazure.tools import is_valid_resource_id
    if namespace.private_cloud:
        if is_valid_resource_id(namespace.private_cloud):
            namespace.private_cloud = namespace.private_cloud.rsplit('/', 1)[-1]


def resource_pool_only_name_validator(namespace):
    """
    Checks whether the passed value is just the resource name (and not the resource id).
    If its the resource id, then the resource name is extracted.
    """
    from msrestazure.tools import is_valid_resource_id
    if namespace.resource_pool:
        if is_valid_resource_id(namespace.resource_pool):
            namespace.resource_pool = namespace.resource_pool.rsplit('/', 1)[-1]


def template_only_name_validator(namespace):
    """
    Checks whether the passed value is just the resource name (and not the resource id).
    If its the resource id, then the resource name is extracted.
    """
    from msrestazure.tools import is_valid_resource_id
    if namespace.template:
        if is_valid_resource_id(namespace.template):
            namespace.template = namespace.template.rsplit('/', 1)[-1]


def vnet_only_name_validator(namespace):
    """
    Checks whether the passed value is just the resource name (and not the resource id).
    If its the resource id, then the resource name is extracted.
    """
    from msrestazure.tools import is_valid_resource_id
    if namespace.virtual_network:
        if is_valid_resource_id(namespace.virtual_network):
            namespace.virtual_network = namespace.virtual_network.rsplit('/', 1)[-1]


def template_name_or_id_validator(cmd, namespace):
    """
    Checks whether the passed value is a valid resource id.
    If not, then assuming that the passed value is a resource name, a resource id is constructed.
    If the constructed resource id is also invalid, an error is raised.
    """
    from azure.cli.core.commands.client_factory import get_subscription_id
    from msrestazure.tools import is_valid_resource_id
    if namespace.template:
        private_cloud = namespace.private_cloud
        if is_valid_resource_id(private_cloud):
            private_cloud = private_cloud.rsplit('/', 1)[-1]
        if not is_valid_resource_id(namespace.template):
            namespace.template = vm_cs_create_resource_id(subscription=get_subscription_id(cmd.cli_ctx),
                                                          namespace='Microsoft.VMwareCloudSimple',
                                                          location=namespace.location,
                                                          resource_type='privateClouds',
                                                          name=private_cloud,
                                                          child_type='virtualmachinetemplates',
                                                          child_name=namespace.template)
    if not is_valid_resource_id(namespace.template):
        raise CLIError('Invalid template.')


def resource_pool_name_or_id_validator(cmd, namespace):
    """
    Checks whether the passed value is a valid resource id.
    If not, then assuming that the passed value is a resource name, a resource id is constructed.
    If the constructed resource id is also invalid, an error is raised.
    """
    from azure.cli.core.commands.client_factory import get_subscription_id
    from msrestazure.tools import is_valid_resource_id
    if namespace.resource_pool:
        private_cloud = namespace.private_cloud
        if is_valid_resource_id(private_cloud):
            private_cloud = private_cloud.rsplit('/', 1)[-1]
        if not is_valid_resource_id(namespace.resource_pool):
            namespace.resource_pool = vm_cs_create_resource_id(subscription=get_subscription_id(cmd.cli_ctx),
                                                               namespace='Microsoft.VMwareCloudSimple',
                                                               location=namespace.location,
                                                               resource_type='privateClouds',
                                                               name=private_cloud,
                                                               child_type='resourcepools',
                                                               child_name=namespace.resource_pool)
    if not is_valid_resource_id(namespace.resource_pool):
        raise CLIError('Invalid resource pool.')


def virtual_network_name_or_id_validator(cmd, client, virtual_network, resource_group_name, vm_name):
    """
    Checks whether the passed value is a valid resource id.
    If not, then assuming that the passed value is a resource name, a resource id is constructed.
    If the constructed resource id is also invalid, an error is raised.
    """
    from azure.cli.core.commands.client_factory import get_subscription_id
    from msrestazure.tools import is_valid_resource_id

    virtual_machine = client.get(resource_group_name, vm_name)

    location = virtual_machine.location
    private_cloud = virtual_machine.private_cloud_id

    if is_valid_resource_id(private_cloud):
        private_cloud = private_cloud.rsplit('/', 1)[-1]
    if not is_valid_resource_id(virtual_network):
        virtual_network = vm_cs_create_resource_id(subscription=get_subscription_id(cmd.cli_ctx),
                                                   namespace='Microsoft.VMwareCloudSimple',
                                                   location=location,
                                                   resource_type='privateClouds',
                                                   name=private_cloud,
                                                   child_type='virtualnetworks',
                                                   child_name=virtual_network)
    if not is_valid_resource_id(virtual_network):
        raise CLIError('Invalid virtual network.')

    return virtual_network