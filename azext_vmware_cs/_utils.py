# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
This file contains generic utility functions.
"""

import os
from knack.util import CLIError
from ._config import PATH_CHAR


def vm_cs_create_resource_id(subscription, namespace, location,
                             resource_type, resource_name, child_type=None,
                             child_name=None):
    """
    Constructs the resource id from the given information (the arguments).
    """
    resource_id = PATH_CHAR + "subscriptions" + PATH_CHAR + subscription + PATH_CHAR + \
        "providers" + PATH_CHAR + namespace + PATH_CHAR + "locations" + \
        PATH_CHAR + location + PATH_CHAR + resource_type + PATH_CHAR + resource_name
    if child_type is not None:
        resource_id = resource_id + PATH_CHAR + child_type
    if child_name is not None:
        resource_id = resource_id + PATH_CHAR + child_name
    return resource_id


def get_vmware_provider():
    """
    Gets the current provider for AVS, from the global configuration file.
    """
    from ._config import (GLOBAL_CONFIG_FILE, GLOBAL_CONFIG_SECTION, CURRENT_PROVIDER_FIELD_NAME)

    from knack.config import get_config_parser

    if not os.path.isfile(GLOBAL_CONFIG_FILE):
        return None

    config = get_config_parser()
    config.read(GLOBAL_CONFIG_FILE)

    if config.has_section(GLOBAL_CONFIG_SECTION):
        return config.get(GLOBAL_CONFIG_SECTION, CURRENT_PROVIDER_FIELD_NAME)
    return None


def vmware_cs_name_or_id_validator(cmd, namespace, resource_type_display_name,
                                   child_type=None, child_resource=None):
    """
    Checks whether the resource is a valid resource id.
    If not, then assuming that the passed value is a resource name, a resource id is constructed.
    If the constructed resource id is also invalid, an error is raised.
    """
    from azure.cli.core.commands.client_factory import get_subscription_id
    from msrestazure.tools import is_valid_resource_id

    if child_type is not None:
        if not is_valid_resource_id(child_resource):
            private_cloud = namespace.private_cloud
            if is_valid_resource_id(private_cloud):
                private_cloud = private_cloud.rsplit('/', 1)[-1]
            resource_id = vm_cs_create_resource_id(subscription=get_subscription_id(cmd.cli_ctx),
                                                   namespace='Microsoft.VMwareCloudSimple',
                                                   location=namespace.location,
                                                   resource_type='privateClouds',
                                                   resource_name=private_cloud,
                                                   child_type=child_type,
                                                   child_name=child_resource)
        else:
            resource_id = child_resource
    else:
        if not is_valid_resource_id(namespace.private_cloud):
            resource_id = vm_cs_create_resource_id(subscription=get_subscription_id(cmd.cli_ctx),
                                                   namespace='Microsoft.VMwareCloudSimple',
                                                   location=namespace.location,
                                                   resource_type='privateClouds',
                                                   resource_name=namespace.private_cloud)
        else:
            resource_id = namespace.private_cloud

    if not is_valid_resource_id(resource_id):
        raise CLIError('Invalid ' + resource_type_display_name + '.')

    return resource_id


def only_resource_name_validator(resource):
    """
    Checks whether the passed value is just the resource name (and not the resource id).
    If its the resource id, then the resource name is extracted.
    """
    from msrestazure.tools import is_valid_resource_id
    if is_valid_resource_id(resource):
        return resource.rsplit('/', 1)[-1]
    return resource


def create_dictionary_from_arg_string(values, option_string=None):
    """
    Creates and returns dictionary from a string containing params in KEY=VALUE format
    """
    params_dict = {}
    for item in values:
        try:
            key, value = item.split('=', 1)
            params_dict[key] = value
        except ValueError:
            raise CLIError('usage error: {} KEY=VALUE [KEY=VALUE ...]'.format(option_string))
    return params_dict
