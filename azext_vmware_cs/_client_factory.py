# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


def cf_vmware_cs(cli_ctx, *_):
    from azure.cli.core.commands.client_factory import get_mgmt_service_client
    from azext_vmware_cs.vendored_sdks import VMwareCloudSimpleClient
    from ._config import (REGION_ID, REFERER)
    return get_mgmt_service_client(cli_ctx,
                                   VMwareCloudSimpleClient,
                                   referer=REFERER,
                                   region_id=REGION_ID)


def cf_virtual_machine(cli_ctx, *_):
    return cf_vmware_cs(cli_ctx).virtual_machine


def cf_private_cloud_by_region(cli_ctx, *_):
    return cf_vmware_cs(cli_ctx).private_cloud_by_region
