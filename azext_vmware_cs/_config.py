# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

'''
Helps in managing the global configuration for AVS, and also the configuration information for AVS by CloudSimple.
'''

from enum import Enum
import os
from azure.cli.core._config import GLOBAL_CONFIG_DIR

# Information to manage global configuration for AVS (stored in config file in .Azure directory)
GLOBAL_CONFIG_FILENAME = 'config'
GLOBAL_CONFIG_FILE = os.path.join(GLOBAL_CONFIG_DIR, GLOBAL_CONFIG_FILENAME)
GLOBAL_CONFIG_SECTION = 'vmware'
CURRENT_PROVIDER_FIELD_NAME = 'current_provider'

# Information to manage configuration information for
# cloudsimple (stored in VMWARE_CS_CONFIG_FILENAME file in this directory)
CONFIG_REGION_SECTION_NAME = 'region'
CONFIG_REGION_FIELD_NAME = 'region_id'
DEFAULT_REGION = ""
VMWARE_CS_CONFIG_FILENAME = "vmware_cs.config"
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
VMWARE_CS_CONFIG_FILE = os.path.join(CURRENT_DIRECTORY, VMWARE_CS_CONFIG_FILENAME)

PATH_CHAR = "/"


def get_region_id():
    """
    Used to extract the region id from the VMWARE_CS_CONFIG_FILENAME file
    """
    from knack.config import get_config_parser

    config = get_config_parser()
    config.read(VMWARE_CS_CONFIG_FILE)

    if not config.has_section(CONFIG_REGION_SECTION_NAME):
        config.add_section(CONFIG_REGION_SECTION_NAME)
        config.set(CONFIG_REGION_SECTION_NAME, CONFIG_REGION_FIELD_NAME, DEFAULT_REGION)
        with open(VMWARE_CS_CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

    return config.get(CONFIG_REGION_SECTION_NAME, CONFIG_REGION_FIELD_NAME)


REGION_ID = get_region_id()
REFERER = "https://management.azure.com/"


# Enum that lists the available providers for AVS
class VmwareProviders(str, Enum):
    """
    The list of available providers in VMware
    """
    CS = "cs"
    VS = "vs"
