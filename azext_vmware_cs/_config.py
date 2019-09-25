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

PATH_CHAR = "/"

REFERER = "https://management.azure.com/"


class VmwareProviders(str, Enum):
    """
    The list of available providers in AVS
    """
    CS = "cs"
    VS = "vs"
