# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
This file contains generic utility functions.
"""

import os
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
