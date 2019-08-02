# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class Sku(Model):
    """The purchase SKU for CloudSimple paid resources.

    All required parameters must be populated in order to send to Azure.

    :param capacity: The capacity of the SKU
    :type capacity: str
    :param description: dedicatedCloudNode example: 8 x Ten-Core Intel® Xeon®
     Processor E5-2640 v4 2.40GHz 25MB Cache (90W); 12 x 64GB PC4-19200 2400MHz
     DDR4 ECC Registered DIMM, ...
    :type description: str
    :param family: If the service has different generations of hardware, for
     the same SKU, then that can be captured here
    :type family: str
    :param name: Required. The name of the SKU for VMWare CloudSimple Node
    :type name: str
    :param tier: The tier of the SKU
    :type tier: str
    """

    _validation = {
        'name': {'required': True},
    }

    _attribute_map = {
        'capacity': {'key': 'capacity', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'family': {'key': 'family', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'tier': {'key': 'tier', 'type': 'str'},
    }

    def __init__(self, *, name: str, capacity: str=None, description: str=None, family: str=None, tier: str=None, **kwargs) -> None:
        super(Sku, self).__init__(**kwargs)
        self.capacity = capacity
        self.description = description
        self.family = family
        self.name = name
        self.tier = tier