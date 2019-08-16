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

    from ._config import (CONFIG_FILE, CONFIG_SECTION, CURRENT_PROVIDER_FIELD_NAME, 
                          AVAILABLE_PROVIDERS_FIELD_NAME)
    import os
    from knack.config import get_config_parser

    if not os.path.isfile(CONFIG_FILE):
        return None

    config = get_config_parser()
    config.read(CONFIG_FILE)

    if config.has_section(CONFIG_SECTION):
        vmware_providers = config.get(CONFIG_SECTION, AVAILABLE_PROVIDERS_FIELD_NAME)
        try:
            current_provider = config.get(CONFIG_SECTION, CURRENT_PROVIDER_FIELD_NAME)
        except:
            raise CLIError('Set a provider using \"az vmware set-provider\" first.')

    if current_provider in vmware_providers:
        return current_provider
