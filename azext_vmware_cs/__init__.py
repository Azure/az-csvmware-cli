# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


from azure.cli.core import AzCommandsLoader

from azext_vmware_cs._help import helps  # pylint: disable=unused-import


class Vmware_csCommandsLoader(AzCommandsLoader):
    """
    Custom command loader (inherited from AzCommandsLoader class) which is used for loading the module.
    """

    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType
        vmware_cs_custom = CliCommandType(operations_tmpl='azext_vmware_cs.custom#{}')
        super(Vmware_csCommandsLoader, self).__init__(cli_ctx=cli_ctx,
                                                      custom_command_type=vmware_cs_custom)

    def load_command_table(self, args):
        from azext_vmware_cs.commands import load_command_table
        load_command_table(self, args)
        return self.command_table

    def load_arguments(self, command):
        from azext_vmware_cs._params import load_arguments
        load_arguments(self, command)


COMMAND_LOADER_CLS = Vmware_csCommandsLoader
