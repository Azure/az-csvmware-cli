# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


from enum import Enum
import os
from azure.cli.core._config import GLOBAL_CONFIG_DIR

CONFIG_FILENAME = 'config'
CONFIG_FILE = os.path.join(GLOBAL_CONFIG_DIR, CONFIG_FILENAME)
CONFIG_SECTION = 'vmware'
CURRENT_PROVIDER_FIELD_NAME = 'current_provider'
AVAILABLE_PROVIDERS_FIELD_NAME = 'available_providers'

class AvailableProviders(str, Enum):
    CS = "cs"
    VS = "vs"

    def list():
        return self.__members__
