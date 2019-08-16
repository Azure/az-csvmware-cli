# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps  # pylint: disable=unused-import


helps['vmware'] = """
    type: group
    short-summary: Commands to manage Azure VMware Solution. To see a provider's commands, you have to set the provider using set-provider command.
"""

helps['vmware set-provider'] = """
    type: group
    short-summary: Set the Azure VMware Solution provider.
"""

helps['vmware get-provider'] = """
    type: group
    short-summary: Returns the Azure VMware Solution provider.
"""
