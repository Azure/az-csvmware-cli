# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
This file contains actions for parsing complex arguments
"""


import argparse
from knack.util import CLIError


class AddNicAction(argparse._AppendAction):
    """
    Action for parsing the nic arguments
    """
    def __call__(self, parser, namespace, values, option_string=None):
        nic_params_dict = {}
        for item in values:
            try:
                key, value = item.split('=', 1)
                nic_params_dict[key] = value
            except ValueError:
                raise CLIError('usage error: {} KEY=VALUE [KEY=VALUE ...]'.format(option_string))

        if namespace.nics:
            namespace.nics.append(nic_params_dict)
        else:
            namespace.nics = [nic_params_dict]


class AddDiskAction(argparse._AppendAction):
    """
    Action for parsing the disk arguments
    """
    def __call__(self, parser, namespace, values, option_string=None):
        disk_params_dict = {}
        for item in values:
            try:
                key, value = item.split('=', 1)
                disk_params_dict[key] = value
            except ValueError:
                raise CLIError('usage error: {} KEY=VALUE [KEY=VALUE ...]'.format(option_string))

        if namespace.disks:
            namespace.disks.append(disk_params_dict)
        else:
            namespace.disks = [disk_params_dict]
