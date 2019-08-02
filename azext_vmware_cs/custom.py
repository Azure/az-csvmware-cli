# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError


def create_vmware_cs(cmd, resource_group_name, vmware_cs_name, location=None, tags=None):
    raise CLIError('TODO: Implement `vmware_cs create`')


def list_vmware_cs(cmd, resource_group_name=None):
    raise CLIError('TODO: Implement `vmware_cs list`')


def update_vmware_cs(cmd, instance, tags=None):
    with cmd.update_context(instance) as c:
        c.set_param('tags', tags)
    return instance