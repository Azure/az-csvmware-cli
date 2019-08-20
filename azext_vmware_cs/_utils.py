# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
This file contains generic utility functions.
"""

import os


def vm_cs_create_resource_id(subscription, namespace, location, resource_type, name, child_type=None, child_name=None):
    """
    Constructs the resource id from the given information (the arguments).
    """
    resource_id = "/subscriptions/" + subscription + "/providers/" + \
                  namespace + "/locations/" + location + "/" + \
                  resource_type + "/" + name
    if child_type is not None:
        resource_id = resource_id + "/" + child_type
    if child_name is not None:
        resource_id = resource_id + "/" + child_name
    return resource_id


def get_vmware_provider():
    """
    Used to get the current provider for AVS, from the global configuration file.
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
