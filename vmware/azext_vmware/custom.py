# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError


def initialize_config():
    import os
    from knack.config import get_config_parser
    from ._config import (CONFIG_FILE, CONFIG_SECTION,
                          AvailableProviders,
                          AVAILABLE_PROVIDERS_FIELD_NAME)
    from azure.cli.core._config import GLOBAL_CONFIG_DIR

    config = get_config_parser()
    config.read(CONFIG_FILE)

    if not config.has_section(CONFIG_SECTION):
        config.add_section(CONFIG_SECTION)

    config.set(CONFIG_SECTION, AVAILABLE_PROVIDERS_FIELD_NAME, str(list(AvailableProviders)))

    if not os.path.isdir(GLOBAL_CONFIG_DIR):
        os.makedirs(GLOBAL_CONFIG_DIR)
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def set_provider(cmd, provider_name):
    import os
    from knack.config import get_config_parser
    from ._config import (CONFIG_FILE, CONFIG_SECTION, CURRENT_PROVIDER_FIELD_NAME, AvailableProviders)
    from azure.cli.core._config import GLOBAL_CONFIG_DIR

    from azure.cli.testsdk.base import ExecutionResult
    

    config = get_config_parser()
    config.read(CONFIG_FILE)

    config.set(CONFIG_SECTION, CURRENT_PROVIDER_FIELD_NAME, provider_name)

    # Installing respective extension
    # if (provider_name == AvailableProviders.CS):
        # exec_result = ExecutionResult(cmd.cli_ctx, 'az extension add -n vmware-cs')
        # try:
        #     exec_result = ExecutionResult(cmd.cli_ctx, 'az extension update -n vmware-cs')
        # except:
        #     pass
    # elif (provider_name == AvailableProviders.VS):
        # exec_result = ExecutionResult(cmd.cli_ctx, 'az extension add -n vmware-vs')
        # try:
        #     exec_result = ExecutionResult(cmd.cli_ctx, 'az extension update -n vmware-vs')
        # except:
        #     pass
    # else:
    #     CLIError("Set provider logic not implemented for ", provider_name)

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def get_provider():
    from ._config import AvailableProviders
    # vmware_provider = get_vmware_provider()

    from ._config import (CONFIG_FILE, CONFIG_SECTION, CURRENT_PROVIDER_FIELD_NAME, 
                          AVAILABLE_PROVIDERS_FIELD_NAME,
                          AvailableProviders)
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
        return AvailableProviders(current_provider)
