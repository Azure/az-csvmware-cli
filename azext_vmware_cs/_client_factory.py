# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
Contains client factory methods used for generating SDK clients.
"""


def cf_vmware_cs(cli_ctx, *_):
    """
    Generic client factory
    """
    from azure.cli.core.commands.client_factory import get_mgmt_service_client

    # This vendored_sdk import is temporary. Import should be from published SDK
    # TODO: Change when production SDK published.
    from azext_vmware_cs.vendored_sdks import VMwareCloudSimpleClient

    from ._config import (REGION_ID, REFERER)
    return get_mgmt_service_client(cli_ctx,
                                   VMwareCloudSimpleClient,
                                   referer=REFERER,
                                   region_id=REGION_ID)
    # The region_id parameter shouldn't be in the client as
    # one subscription could have avs in multiple regions.
    # This is a swagger issue which is being followed on.
    # TODO: Remove after swagger issue fixed


def cf_virtual_machine(cli_ctx, *_):
    """
    Client factory for VM operations
    """
    return cf_vmware_cs(cli_ctx).virtual_machine


def cf_private_cloud_by_region(cli_ctx, *_):
    """
    Client factory for private cloud by region operations
    """
    return cf_vmware_cs(cli_ctx).private_cloud_by_region


def _resource_client_factory(cli_ctx, **_):
    """
    Client factory for resource client
    """
    from azure.cli.core.commands.client_factory import get_mgmt_service_client
    from azure.cli.core.profiles import ResourceType
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES)


def cf_resource_groups(cli_ctx, *_):
    """
    Client factory for resource group operations
    """
    return _resource_client_factory(cli_ctx).resource_groups
