# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


def load_command_table(self, _):

    with self.command_group('vmware', is_preview=True) as g:
        g.custom_command('set-provider', 'set_provider')
        g.custom_command('get-provider', 'get_provider')
