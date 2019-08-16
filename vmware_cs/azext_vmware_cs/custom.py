# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


from knack.util import CLIError


def list_private_cloud_by_region(client):
    return client.list()


def set_region(client, region_name):
    from knack.config import get_config_parser
    from ._config import (VMWARE_LOCAL_CONFIG_FILE, CONFIG_REGION, CONFIG_REGION_ID)

    config = get_config_parser()
    config.read(VMWARE_LOCAL_CONFIG_FILE)

    if not config.has_section(CONFIG_REGION):
        config.add_section(CONFIG_REGION)

    config.set(CONFIG_REGION, CONFIG_REGION_ID, region_name)

    with open(VMWARE_LOCAL_CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

    client.config.region_id = region_name


def get_region():
    from ._config import get_region_id
    return get_region_id()


def list_resource_pool_by_PC(client, private_cloud, resource_pool=None):
    if resource_pool is None:
        return client.resource_pools_by_pc.list(private_cloud)
    return client.resource_pool_by_pc.get(private_cloud, resource_pool)


def list_virtual_networks(client, private_cloud, resource_pool=None, virtual_network=None):
    if (((resource_pool is None) and (virtual_network is None)) or
            ((resource_pool is not None) and (virtual_network is not None))):
        raise CLIError('Enter either a resource pool or a virtual network.')

    if resource_pool is not None:
        return client.virtual_networks_by_pc.list(private_cloud, resource_pool)
    return client.virtual_network_by_pc.get(private_cloud, virtual_network)


# --------------------------------------------------------------------------------------------
# Virtual Machine APIs
# --------------------------------------------------------------------------------------------

def create_vmware_cs_vm(client, location, resource_group_name, vm_name,
                        private_cloud, template, resource_pool,
                        amount_of_ram=1024, number_of_cores=1):
    from .vendored_sdks.models.virtual_machine import VirtualMachine
    from .vendored_sdks.models.resource_pool import ResourcePool

    resource_pool = ResourcePool(id=resource_pool)
    virtual_machine = VirtualMachine(location=location,
                                     amount_of_ram=amount_of_ram,
                                     guest_os="guest_os",
                                     guest_os_type="other",
                                     number_of_cores=number_of_cores,
                                     private_cloud_id=private_cloud,
                                     resource_pool=resource_pool,
                                     template_id=template)

    return client.create_or_update(resource_group_name, vm_name, virtual_machine)


def add_vmware_cs_vnic(cmd, client, resource_group_name, vm_name,
                       virtual_network, adapter="VMXNET3", power_on_boot=False):
    from .vendored_sdks.models.virtual_nic import VirtualNic
    from .vendored_sdks.models.virtual_network import VirtualNetwork
    from ._validators import virtual_network_name_or_id_validator

    virtual_machine = client.get(resource_group_name, vm_name)
    virtual_network = virtual_network_name_or_id_validator(cmd, client, virtual_network, resource_group_name, vm_name)

    network = VirtualNetwork(id=virtual_network)
    nic = VirtualNic(network=network,
                     nic_type=adapter,
                     power_on_boot=power_on_boot)

    virtual_machine.nics.append(nic)
    return client.create_or_update(resource_group_name, vm_name, virtual_machine)


def add_vmware_cs_vdisk(client, resource_group_name, vm_name, controller="1000",
                        independence_mode="persistent", size=16777216):
    from .vendored_sdks.models.virtual_disk import VirtualDisk

    virtual_machine = client.get(resource_group_name, vm_name)
    disk = VirtualDisk(controller_id=controller,
                       independence_mode=independence_mode,
                       total_size=size)

    virtual_machine.disks.append(disk)
    return client.create_or_update(resource_group_name, vm_name, virtual_machine)


def list_vmware_cs_vm(client, resource_group_name=None):
    if resource_group_name is None:
        return client.list_by_subscription()
    return client.list_by_resource_group(resource_group_name)


def list_vm_template_by_PC(client, private_cloud, resource_pool=None, template=None):
    if (((resource_pool is None) and (template is None)) or
            ((resource_pool is not None) and (template is not None))):
        raise CLIError('Enter either a resource pool or a virtual machine template.')

    if resource_pool is not None:
        return client.virtual_machine_templates_by_pc.list(private_cloud, resource_pool)
    return client.virtual_machine_template_by_pc.get(private_cloud, template)


def delete_vmware_cs_vm(client, resource_group_name, vm_name):
    return client.delete(resource_group_name, vm_name)


def get_vmware_cs_vm(client, resource_group_name, vm_name):
    return client.get(resource_group_name, vm_name)


def start_vmware_cs_vm(client, resource_group_name, vm_name):
    return client.start(resource_group_name, vm_name)


def stop_vmware_cs_vm(client, resource_group_name, vm_name, stop_mode):
    return client.stop(resource_group_name, vm_name, stop_mode)


def update_vmware_cs_vm(client, resource_group_name, vm_name, **kwargs):
    return client.update(resource_group_name, vm_name, kwargs['parameters'].tags)
