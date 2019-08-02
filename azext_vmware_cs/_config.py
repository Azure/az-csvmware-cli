# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


from enum import Enum
import os
from azure.cli.core._config import GLOBAL_CONFIG_DIR

VMWARE_CONFIG_FILENAME = 'vmware.config'
VMWARE_CONFIG_FILE = os.path.join(GLOBAL_CONFIG_DIR, VMWARE_CONFIG_FILENAME)
CONFIG_VMWARE = 'vmware'
CONFIG_PROVIDER = 'provider'
CONFIG_REGION = 'region'
CONFIG_REGION_ID = 'region_id'
DEFAULT_REGION = "eastus"

VMWARE_LOCAL_CONFIG_FILENAME = "local_config.config"
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
VMWARE_LOCAL_CONFIG_FILE = os.path.join(CURRENT_DIRECTORY, VMWARE_LOCAL_CONFIG_FILENAME)


def get_region_id():
    from knack.config import get_config_parser

    config = get_config_parser()
    config.read(VMWARE_LOCAL_CONFIG_FILE)

    if not config.has_section(CONFIG_REGION):
        config.add_section(CONFIG_REGION)
        config.set(CONFIG_REGION, CONFIG_REGION_ID, DEFAULT_REGION)
        with open(VMWARE_LOCAL_CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

    return config.get(CONFIG_REGION, CONFIG_REGION_ID)


REGION_ID = get_region_id()
REFERER = "https://management.azure.com/"


class VmwareProviders(str, Enum):
    CS = "cs"
    VS = "vs"
