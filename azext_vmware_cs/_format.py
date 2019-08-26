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

    transformed_result = OrderedDict([('Resource group', result['resourceGroup']),
                                      ('Computer name', result['name']),
                                      ('Status', result['status']),
                                      ('Operating system', result['guestOs']),
                                      ('Location', result['location']),
                                      ('Size', str(result['numberOfCores']) + " cores, " +
                                       str(result['amountOfRam']) + " MB memory"),
                                      ('Public IP/DNS name', str(result['publicIp']) +
                                       "/" + str(result['dnsname'])),
                                      ('Subscription ID', result['id'].split('/')[2]),
                                      ('Resource Pool', result['resourcePool']['fullName']),
                                      ('vSphere folder', result['folder']),
                                      ('VMware Tools', result['vmwaretools'])])

    if result['nics']:
        nics = result['nics']
        ipAddresses = ""
        notnull = False
        for nic in nics:
            if nic['ipAddresses'] is not None:
                notnull = True
                for ipaddress in nic['ipAddresses']:
                    ipAddresses = ipAddresses + ipaddress + ", "
        if notnull:
            ipAddresses = ipAddresses[:-2]
            transformed_result['IP Addresses'] = ipAddresses

    if result['nics']:
        nics = result['nics']
        vSphereNetworks = ""
        for nic in nics:
            vSphereNetworks = vSphereNetworks + nic['network']['name'] + ", "
        vSphereNetworks = vSphereNetworks[:-2]
        transformed_result['vSphere Networks'] = vSphereNetworks

    return transformed_result
