# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from azure.cli.core.commands.parameters import get_enum_type
from ._config import AvailableProviders

def load_arguments(self, _):

    with self.argument_context('vmware') as c:
        c.argument('provider_name', options_list=['--name', '-n'],
                   help="Name of the Azure VMware Service provider.",
                   arg_type=get_enum_type(AvailableProviders))
