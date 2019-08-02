# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


import os


def vm_cs_create_resource_id(subscription, namespace, location, resource_type, name, child_type=None, child_name=None):
    resource_id = "/subscriptions/" + subscription + "/providers/" + \
                  namespace + "/locations/" + location + "/" + \
                  resource_type + "/" + name
    if child_type is not None:
        resource_id = resource_id + "/" + child_type
    if child_name is not None:
        resource_id = resource_id + "/" + child_name
    return resource_id


def get_vmware_provider():
    from ._config import (VMWARE_CONFIG_FILE, CONFIG_VMWARE, CONFIG_PROVIDER)

    from knack.config import get_config_parser

    if not os.path.isfile(VMWARE_CONFIG_FILE):
        return None

    config = get_config_parser()
    config.read(VMWARE_CONFIG_FILE)

    if config.has_section(CONFIG_VMWARE):
        return config.get(CONFIG_VMWARE, CONFIG_PROVIDER)
    return None
