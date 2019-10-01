# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
This file contains the custom methods which are executed whenever any command is called.
The custom methods are linked to the commands at the time of command registeration (commands.py).
"""


from knack.util import CLIError


def list_private_cloud(client, location):
    """
    Returns a list of private clouds in a region.
    """
    return client.list(location)


def show_private_cloud(client, private_cloud, location):
    """
    Get the details of a private cloud.
    """
    return client.get(private_cloud, location)


def list_resource_pool(client, private_cloud, location):
    """
    Returns the list of resource pool in the specified private cloud.
    """
    return client.list(location, private_cloud)


def show_resource_pool(client, private_cloud, resource_pool, location):
    """
    Returns the details of a resource pool.
    """
    return client.get(location, private_cloud, resource_pool)


def list_virtual_networks(client, private_cloud, resource_pool, location):
    """
    Returns the list of available virtual networks in a resource pool, in a private cloud.
    """
    return client.list(location, private_cloud, resource_pool)


def show_virtual_network(client, private_cloud, virtual_network, location):
    """
    Returns the details of a virtual network in a private cloud.
    """
    return client.get(location, private_cloud, virtual_network)


def list_vm_template(client, private_cloud, resource_pool, location):
    """
    Returns the list of VMware virtual machines templates in a resource pool, in a private cloud.
    """
    return client.list(private_cloud, location, resource_pool)


def show_vm_template(client, private_cloud, template, location):
    """
    Returns details of a VMware virtual machines template in a private cloud.
    """
    return client.get(location, private_cloud, template)


# --------------------------------------------------------------------------------------------
# Virtual Machine APIs
# --------------------------------------------------------------------------------------------

def _modify_template_disks_according_to_input(template_disks, input_disks):
    """
    Change template disks according to the input given by the user.
    """

    # Populating the disk names of vm-template in a dictionary,
    # and mapping them to their index in _nics list
    vm_template_disk_names = {}
    for (i, disk) in enumerate(template_disks):
        vm_template_disk_names[disk.virtual_disk_name] = i

    from .vendored_sdks.models.virtual_disk import VirtualDisk

    # Check if disks entered by the user exist in vm-template,
    # then override the properties specified. Else create a new disk.
    for disk in input_disks:
        if disk['name'] in vm_template_disk_names.keys():
            index = vm_template_disk_names[disk['name']]
            if 'controller' in disk.keys():
                template_disks[index].controller_id = disk['controller']
            if 'mode' in disk.keys():
                template_disks[index].independence_mode = disk['mode']
            if 'size' in disk.keys():
                template_disks[index].total_size = disk['size']
            # template_disks[index].virtual_disk_id = None

        else:
            disk_name = disk['name']
            if 'controller' in disk.keys():
                controller = disk['controller']
            else:
                raise CLIError('controller parameter not specified for disk ' + disk_name + ".")
            if 'mode' in disk.keys():
                mode = disk['mode']
            else:
                raise CLIError('mode parameter not specified for disk ' + disk_name + ".")
            if 'size' in disk.keys():
                size = disk['size']
            else:
                raise CLIError('size parameter not specified for disk ' + disk_name + ".")

            disk_object = VirtualDisk(controller_id=controller,
                                      independence_mode=mode,
                                      total_size=size)
            template_disks.append(disk_object)
    return template_disks


def _modify_template_nics_according_to_input(template_nics, input_nics, cmd, client,
                                             resource_group_name, vm_name,
                                             location, private_cloud):
    """
    Change template nics according to the input given by the user.
    """
    # Populating the nic names of vm-template in a dictionary,
    # and mapping them to their index in _nics list
    vm_template_nic_names = {}
    for (i, nic) in enumerate(template_nics):
        vm_template_nic_names[nic.virtual_nic_name] = i

    from .vendored_sdks.models.virtual_nic import VirtualNic
    from .vendored_sdks.models.virtual_network import VirtualNetwork
    from ._validators import virtual_network_name_or_id_validator

    # Check if nics entered by a user exist in vm-template,
    # then override the properties specified. Else create a new nic.
    for nic in input_nics:
        if nic['name'] in vm_template_nic_names.keys():
            index = vm_template_nic_names[nic['name']]
            if 'virtual-network' in nic.keys():
                template_nics[index].network.id = nic['virtual-network']
            if 'adapter' in nic.keys():
                template_nics[index].nic_type = nic['adapter']
            if 'power-on-boot' in nic.keys():
                template_nics[index].power_on_boot = nic['power-on-boot']
            template_nics[index].virtual_nic_id = None

        else:
            nic_name = nic['name']
            if 'virtual-network' in nic.keys():
                vnet = nic['virtual-network']
            else:
                raise CLIError('virtual-network parameter not specified for nic ' +
                               nic_name + ".")
            if 'adapter' in nic.keys():
                adapter = nic['adapter']
            else:
                raise CLIError('adapter parameter not specified for nic ' +
                               nic_name + ".")
            if 'power-on-boot' in nic.keys():
                power_on_boot = nic['power-on-boot']
            else:
                raise CLIError('power-on-boot parameter not specified for nic ' +
                               nic_name + ".")

            vnet = virtual_network_name_or_id_validator(cmd, client, vnet,
                                                        resource_group_name, vm_name,
                                                        location, private_cloud)
            network = VirtualNetwork(id=vnet)
            nic_object = VirtualNic(network=network,
                                    nic_type=adapter,
                                    power_on_boot=power_on_boot)
            template_nics.append(nic_object)
    return template_nics


def create_vm(cmd, client, resource_group_name, vm_name,
              private_cloud, template, resource_pool,
              amount_of_ram=None, number_of_cores=None,
              location=None, expose_to_guest_vm=None,
              nics=None, disks=None):
    """
    Create or update a VMware virtual machine.
    The vm-template specified is used as a template for creation.
    """
    from .vendored_sdks.models.virtual_machine import VirtualMachine
    from .vendored_sdks.models.resource_pool import ResourcePool

    resource_pool = ResourcePool(id=resource_pool)

    # Extracting template and private cloud name from the resource id
    template_name = template.rsplit('/', 1)[-1]
    private_cloud_name = private_cloud.rsplit('/', 1)[-1]
    vm_template = client.virtual_machine_templates.get(location, private_cloud_name, template_name)

    cores = number_of_cores or vm_template.number_of_cores
    ram = amount_of_ram or vm_template.amount_of_ram
    if expose_to_guest_vm is None:
        expose = vm_template.expose_to_guest_vm
    else:
        expose = expose_to_guest_vm

    final_disks = vm_template.disks

    if disks is not None:
        final_disks = _modify_template_disks_according_to_input(final_disks, disks)

    final_nics = vm_template.nics

    if nics is not None:
        final_nics = _modify_template_nics_according_to_input(final_nics, nics, cmd, client,
                                                              resource_group_name, vm_name,
                                                              location, private_cloud)

    virtual_machine = VirtualMachine(location=location,
                                     amount_of_ram=ram,
                                     disks=final_disks,
                                     expose_to_guest_vm=expose,
                                     nics=final_nics,
                                     number_of_cores=cores,
                                     private_cloud_id=private_cloud,
                                     resource_pool=resource_pool,
                                     template_id=template)

    return client.virtual_machines.create_or_update(resource_group_name, vm_name, virtual_machine)


def list_vm(client, resource_group_name=None):
    """
    Returns a list of VMware virtual machines in the current subscription.
    If resource group is specified, only the virtual machines
    in that resource group would be listed.
    """
    if resource_group_name is None:
        return client.list_by_subscription()
    return client.list_by_resource_group(resource_group_name)


def delete_vm(client, resource_group_name, vm_name):
    """
    Delete a VMware virtual machine.
    """
    return client.delete(resource_group_name, vm_name)


def get_vm(client, resource_group_name, vm_name):
    """
    Returns a VMware virtual machine.
    """
    return client.get(resource_group_name, vm_name)


def start_vm(client, resource_group_name, vm_name):
    """
    Start a VMware virtual machine.
    """
    return client.start(resource_group_name, vm_name)


def stop_vm(client, resource_group_name, vm_name, stop_mode):
    """
    Stop a VMware virtual machine.
    """
    return client.stop(resource_group_name, vm_name, stop_mode)


def update_vm(client, resource_group_name, vm_name, **kwargs):
    """
    Update VMware virtual machine tags.
    """
    return client.update(resource_group_name, vm_name, kwargs['parameters'].tags)


# --------------------------------------------------------------------------------------------
# VM nics APIs
# --------------------------------------------------------------------------------------------

def add_vnic(cmd, client, resource_group_name, vm_name,
             virtual_network, adapter="VMXNET3", power_on_boot=False):
    """
    Add virtual network interface to a VMware virtual machine.
    """
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


def list_vnics(client, resource_group_name, vm_name):
    """
    List details of a VMware virtual machine's nics.
    """
    virtual_machine = client.get(resource_group_name, vm_name)
    return virtual_machine.nics


def show_vnic(client, resource_group_name, vm_name, nic_name):
    """
    Get the details of a VMware virtual machine's NIC.
    """
    virtual_machine = client.get(resource_group_name, vm_name)
    nics = virtual_machine.nics
    for nic in nics:
        if nic.virtual_nic_name == nic_name:
            return nic
    return None


def delete_vnics(client, resource_group_name, vm_name, nic_names):
    """
    Delete NICs from a VM.
    """
    import copy
    virtual_machine = client.get(resource_group_name, vm_name)

    # Dictionary to maintain the nics to delete
    to_delete_nics = {}
    for nic_name in nic_names:
        to_delete_nics[nic_name] = True

    nics = virtual_machine.nics
    final_nics = copy.deepcopy(nics)
    for nic in nics:
        if nic.virtual_nic_name in to_delete_nics.keys():
            final_nics.remove(nic)
            to_delete_nics[nic.virtual_nic_name] = False

    virtual_machine.nics = final_nics
    client.create_or_update(resource_group_name, vm_name, virtual_machine)

    not_deleted_nics = ""
    for nic_name in to_delete_nics:
        if to_delete_nics[nic_name]:
            not_deleted_nics = not_deleted_nics + nic_name + ", "
    not_deleted_nics = not_deleted_nics[:-2]
    if not_deleted_nics != "":
        raise CLIError(not_deleted_nics + ' not present in the given virtual machine. Other nics (if mentioned) were deleted.')


# --------------------------------------------------------------------------------------------
# VM disks APIs
# --------------------------------------------------------------------------------------------

def add_vdisk(client, resource_group_name, vm_name, controller="1000",
              independence_mode="persistent", size=16777216):
    """
    Add disk to a VMware virtual machine
    """
    from .vendored_sdks.models.virtual_disk import VirtualDisk

    virtual_machine = client.get(resource_group_name, vm_name)
    disk = VirtualDisk(controller_id=controller,
                       independence_mode=independence_mode,
                       total_size=size)

    virtual_machine.disks.append(disk)
    return client.create_or_update(resource_group_name, vm_name, virtual_machine)


def list_vdisks(client, resource_group_name, vm_name):
    """
    List details of disks available on a VMware virtual machine.
    """
    virtual_machine = client.get(resource_group_name, vm_name)
    return virtual_machine.disks


def show_vdisk(client, resource_group_name, vm_name, disk_name):
    """
    Get the details of a VMware virtual machine's disk.
    """
    virtual_machine = client.get(resource_group_name, vm_name)
    disks = virtual_machine.disks
    for disk in disks:
        if disk.virtual_disk_name == disk_name:
            return disk
    return None


def delete_vdisks(client, resource_group_name, vm_name, disk_names):
    """
    Delete disks from a VM.
    """
    import copy
    virtual_machine = client.get(resource_group_name, vm_name)

    # Dictionary to maintain the disks to delete
    to_delete_disks = {}
    for disk_name in disk_names:
        to_delete_disks[disk_name] = True

    disks = virtual_machine.disks
    final_disks = copy.deepcopy(disks)
    for disk in disks:
        if disk.virtual_disk_name in to_delete_disks.keys():
            final_disks.remove(disk)
            to_delete_disks[disk.virtual_disk_name] = False

    virtual_machine.disks = final_disks
    client.create_or_update(resource_group_name, vm_name, virtual_machine)

    not_deleted_disks = ""
    for disk_name in to_delete_disks:
        if to_delete_disks[disk_name]:
            not_deleted_disks = not_deleted_disks + disk_name + ", "
    not_deleted_disks = not_deleted_disks[:-2]
    if not_deleted_disks != "":
        raise CLIError(not_deleted_disks + ' not present in the given virtual machine. Other disks (if mentioned) were deleted.')
