# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
This file contains table transformer functions.
These are called if the output mode is set to table in any command.
"""


def transform_vm_table_output(result):
    """
    This table output contains most of the fields which
    are displayed in CloudSimple VM summary in UI
    """
    from collections import OrderedDict
    from ._config import PATH_CHAR

    transformed_result = OrderedDict([('Resource group', result['resourceGroup']),
                                      ('Computer name', result['name']),
                                      ('Status', result['status']),
                                      ('Operating system', result['guestOs']),
                                      ('Location', result['location']),
                                      ('Size', str(result['numberOfCores']) + " cores, " +
                                       str(result['amountOfRam']) + " MB memory"),
                                      ('Public IP' + PATH_CHAR + 'DNS name', str(result['publicIp']) +
                                       PATH_CHAR + str(result['dnsname'])),
                                      ('Subscription ID', result['id'].split(PATH_CHAR)[2]),
                                      ('Resource Pool', result['resourcePool']['fullName']),
                                      ('vSphere folder', result['folder']),
                                      ('VMware Tools', result['vmwaretools'])])

    ipAddresses = ""
    notnull = False
    for nic in result['nics']:
        if nic['ipAddresses'] is not None:
            notnull = True
            for ipaddress in nic['ipAddresses']:
                ipAddresses = ipAddresses + ipaddress + ", "
    if notnull:
        ipAddresses = ipAddresses[:-2]
        transformed_result['IP Addresses'] = ipAddresses

    vSphereNetworks = ""
    notnull = False
    for nic in result['nics']:
        if nic['network']['name'] is not None:
            notnull = True
            vSphereNetworks = vSphereNetworks + nic['network']['name'] + ", "
    if notnull:
        vSphereNetworks = vSphereNetworks[:-2]
        transformed_result['vSphere Networks'] = vSphereNetworks

    return transformed_result


def transform_vm_table_list(vm_list):
    """
    For list output
    """
    return [transform_vm_table_output(v) for v in vm_list]
