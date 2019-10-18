# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import unittest

from knack.util import CLIError
from azure_devtools.scenario_tests import AllowLargeResponse
from azure.cli.testsdk import (ScenarioTest, ResourceGroupPreparer)
from msrestazure.azure_exceptions import CloudError
import logging

TEST_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))


class VmwareCsScenarioTest(ScenarioTest):
    """
    Test for AVS by CloudSimple CLI commands.
    This tests various command exposed by CloudSimple CLI.
    To run the tests, run 'azdev test vmware-cs --discover --live'

    The prerequisites for the tests are that you should be logged in to a subscription in the CLI.
    That subscription should contain:
    az_cli_cs_test resource group,
    avs-test-eastus private cloud,
    vm-125 vm template in vSphere,
    resgroup-169 resource pool in vSphere,
    dvportgroup-85 virtual network.

    You can modify the above specified params in this test file.
    """

    @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    def test_vmware_cs_vm_create_param_validation(self, resource_group):
        """
        Tests the create API for vmware vm.
        """

        self.kwargs.update({
            'name': self.create_random_name(prefix='cli-test', length=24),
            'loc': 'eastus',
            'pc': 'avs-test-eastus',
            'vm_template': 'vm-125',
            'rp': 'resgroup-169',
            'ram': 1024,
            'cores': 1
        })

        # Checking that invalid vm_name causes error
        with self.assertRaisesRegexp(CLIError, "Virtual machine name should only contain letters, numbers, or hyphen."):
            self.cmd('az vmware vm create -g {rg} -n invalid_name# --location {loc} --ram {ram} \
                 --cores {cores} --private-cloud {pc} --template {vm_template} \
                 --resource-pool {rp}')

        # Checking that if entered value for ram is float, it causes error
        with self.assertRaisesRegexp(CLIError, "RAM should be a postive integer value."):
            self.cmd('az vmware vm create -g {rg} -n {name} --location {loc} --ram 1024.5 \
                 --cores {cores} --private-cloud {pc} --template {vm_template} \
                 --resource-pool {rp}')

        # Checking that if entered value for ram is 0, it causes error
        with self.assertRaisesRegexp(CLIError, "RAM should be a postive integer value."):
            self.cmd('az vmware vm create -g {rg} -n {name} --location {loc} --ram 0 \
                 --cores {cores} --private-cloud {pc} --template {vm_template} \
                 --resource-pool {rp}')

        # Checking that if entered value for ram is negative, it causes error
        with self.assertRaisesRegexp(CLIError, "RAM should be a postive integer value."):
            self.cmd('az vmware vm create -g {rg} -n {name} --location {loc} --ram -1024 \
                 --cores {cores} --private-cloud {pc} --template {vm_template} \
                 --resource-pool {rp}')

        # Checking that if entered value for cores is float, it causes error
        with self.assertRaisesRegexp(CLIError, "Cores should be a postive integer value."):
            self.cmd('az vmware vm create -g {rg} -n {name} --location {loc} --ram {ram} \
                 --cores 1.5 --private-cloud {pc} --template {vm_template} \
                 --resource-pool {rp}')

        # Checking that if entered value for cores is 0, it causes error
        with self.assertRaisesRegexp(CLIError, "Cores should be a postive integer value."):
            self.cmd('az vmware vm create -g {rg} -n {name} --location {loc} --ram {ram} \
                 --cores 0 --private-cloud {pc} --template {vm_template} \
                 --resource-pool {rp}')

        # Checking that if entered value for cores is negative, it causes error
        with self.assertRaisesRegexp(CLIError, "Cores should be a postive integer value."):
            self.cmd('az vmware vm create -g {rg} -n {name} --location {loc} --ram {ram} \
                 --cores -1 --private-cloud {pc} --template {vm_template} \
                 --resource-pool {rp}')

    @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    def test_vmware_cs_vm_crud(self, resource_group):
        """
        Tests the CRUD APIs for vmware vm.
        """

        self.kwargs.update({
            'name': self.create_random_name(prefix='cli-test1', length=24),
            'loc': 'eastus',
            'pc': 'avs-test-eastus',
            'vm_template': 'vm-125',
            'rp': 'resgroup-169',
            'ram': 1024,
            'cores': 1
        })

        # Checking that the number of VM in our rg (used for testing) is 0.
        count = len(self.cmd('az vmware vm list -g {rg}').get_output_in_json())
        self.assertEqual(count, 0)

        # Creating a VM. Checking json to see if the operation succeeded.
        self.cmd('az vmware vm create -g {rg} -n {name} --location {loc} --ram {ram} \
                 --cores {cores} --private-cloud {pc} --template {vm_template} \
                 --resource-pool {rp}',
                 checks=[
                     self.check('provisioningState', 'Succeeded'),
                     self.check('resourceGroup', '{rg}'),
                     self.check('name', '{name}'),
                     self.check('amountOfRam', '{ram}'),
                     self.check('location', '{loc}')
                 ])

        # Checking that the number of VM in our rg (used for testing) is 1 now.
        count = len(self.cmd('az vmware vm list -g {rg}').get_output_in_json())
        self.assertEqual(count, 1)

        # Testing show command
        self.cmd('az vmware vm show -g {rg} -n {name}',
                 checks=[
                     self.check('provisioningState', 'Succeeded'),
                     self.check('resourceGroup', '{rg}'),
                     self.check('name', '{name}'),
                     self.check('amountOfRam', '{ram}'),
                     self.check('location', '{loc}')
                 ])

        # Show as table
        self.cmd('az vmware vm show -g {rg} -n {name} -o table')

        # List as table
        self.cmd('az vmware vm list -g {rg} -o table')

        # Testing update command
        self.cmd('az vmware vm update -g {rg} -n {name} --set tags.foo=boo', checks=[
            self.check('tags.foo', 'boo')
        ])

        # Deleting a VM.
        self.cmd('az vmware vm delete -g {rg} -n {name}')

        # Checking that the number of VM in our rg is 0 now.
        count = len(self.cmd('az vmware vm list -g {rg}').get_output_in_json())
        self.assertEqual(count, 0)

    def test_vmware_cs_vm_create(self):
        """
        Tests the create API for vmware vm.
        """

        self.kwargs.update({
            'name1': self.create_random_name(prefix='cli-test', length=24),
            'name2': self.create_random_name(prefix='cli-test', length=24),
            'name3': self.create_random_name(prefix='cli-test', length=24),
            'name4': self.create_random_name(prefix='cli-test', length=24),
            'name5': self.create_random_name(prefix='cli-test', length=24),
            'name6': self.create_random_name(prefix='cli-test', length=24),
            'rg': 'az_cli_cs_test',
            'pc': 'avs-test-eastus',
            'vm_template': 'vm-125',
            'rp': 'resgroup-169',
            'vnet': 'dvportgroup-85'
        })

        # Creating a VM with default parameters from the vm template
        self.cmd('az vmware vm create -g {rg} -n {name1} -p {pc} --template {vm_template} -r {rp}',
                 checks=[
                     self.check('provisioningState', 'Succeeded'),
                     self.check('resourceGroup', '{rg}'),
                     self.check('name', '{name1}'),
                     self.check('amountOfRam', 1024),
                     self.check('disks | [0].virtualDiskName', 'Hard disk 1'),
                     self.check('guestOs', 'Ubuntu Linux (64-bit)'),
                     self.check('guestOsType', 'linux'),
                     self.check('location', 'eastus'),
                     self.check('nics | [0].virtualNicName', 'Network adapter 1'),
                     self.check('numberOfCores', 1)
                 ])

        # Creating a VM with default parameters from the vm template and adding a nic
        self.cmd('az vmware vm create -g {rg} -n {name2} \
                 -p {pc} --template {vm_template} -r {rp} \
                 --nic name=NicNameWouldBeReassigned virtual-network={vnet} \
                 adapter=VMXNET3 power-on-boot=True',
                 checks=[
                     self.check('provisioningState', 'Succeeded'),
                     self.check('resourceGroup', '{rg}'),
                     self.check('name', '{name2}'),
                     self.check('amountOfRam', 1024),
                     self.check('disks | [0].virtualDiskName', 'Hard disk 1'),
                     self.check('guestOs', 'Ubuntu Linux (64-bit)'),
                     self.check('guestOsType', 'linux'),
                     self.check('location', 'eastus'),
                     self.check('nics | [0].virtualNicName', 'Network adapter 1'),
                     self.check('nics | [1].virtualNicName', 'Network adapter 2'),
                     self.check('nics | [1].powerOnBoot', True),
                     self.check('nics | [1].nicType', 'VMXNET3'),
                     self.check('nics | [1].network.name', 'Datacenter/Workload01'),
                     self.check('numberOfCores', 1)
                 ])

        # Customizing specific properties of a VM. Changing the number of cores to 2 and adapter of
        # "Network adapter 1" nic to E1000E, from that specified in the template.
        self.cmd('az vmware vm create -n {name3} -g {rg} -p {pc} -r {rp} --template {vm_template} \
                 --cores 2 --nic name="Network adapter 1" adapter=E1000E',
                 checks=[
                     self.check('provisioningState', 'Succeeded'),
                     self.check('resourceGroup', '{rg}'),
                     self.check('name', '{name3}'),
                     self.check('amountOfRam', 1024),
                     self.check('disks | [0].virtualDiskName', 'Hard disk 1'),
                     self.check('guestOs', 'Ubuntu Linux (64-bit)'),
                     self.check('guestOsType', 'linux'),
                     self.check('location', 'eastus'),
                     self.check('nics | [0].virtualNicName', 'Network adapter 1'),
                     self.check('nics | [0].nicType', 'E1000E'),
                     self.check('numberOfCores', 2)
                 ])

        # Customizing specific properties of a VM. Changing the adapter of
        # "Network adapter 1" nic to E1000E, from that specified in the
        # template, and also adding another nic with virtual network
        # MyVirtualNetwork, adapter VMXNET3, that power ups on boot.
        self.cmd('az vmware vm create -g {rg} -n {name4} \
                 -p {pc} --template {vm_template} -r {rp} \
                 --nic name="Network adapter 1" adapter=E1000E --nic \
                 name=NicNameWouldBeReassigned virtual-network={vnet} \
                 adapter=VMXNET3 power-on-boot=True',
                 checks=[
                     self.check('provisioningState', 'Succeeded'),
                     self.check('resourceGroup', '{rg}'),
                     self.check('name', '{name4}'),
                     self.check('amountOfRam', 1024),
                     self.check('disks | [0].virtualDiskName', 'Hard disk 1'),
                     self.check('guestOs', 'Ubuntu Linux (64-bit)'),
                     self.check('guestOsType', 'linux'),
                     self.check('location', 'eastus'),
                     self.check('nics | [0].virtualNicName', 'Network adapter 1'),
                     self.check('nics | [0].nicType', 'E1000E'),
                     self.check('nics | [1].virtualNicName', 'Network adapter 2'),
                     self.check('nics | [1].powerOnBoot', True),
                     self.check('nics | [1].nicType', 'VMXNET3'),
                     self.check('nics | [1].network.name', 'Datacenter/Workload01'),
                     self.check('numberOfCores', 1)
                 ])

        # Creating a virtual machine and adding an extra disk
        # to the VM with SCSI controller 0, persistent
        # mode, and 41943040 KB size.
        self.cmd('az vmware vm create -n {name5} -g {rg} -p {pc} -r {rp} --template {vm_template} \
                 --disk name=DiskNameWouldBeReassigned controller=1000 \
                 mode=persistent size=41943040',
                 checks=[
                     self.check('provisioningState', 'Succeeded'),
                     self.check('resourceGroup', '{rg}'),
                     self.check('name', '{name5}'),
                     self.check('amountOfRam', 1024),
                     self.check('disks | [0].virtualDiskName', 'Hard disk 1'),
                     self.check('disks | [1].controllerId', '1000'),
                     self.check('disks | [1].independenceMode', 'persistent'),
                     self.check('disks | [1].totalSize', 41943040),
                     self.check('guestOs', 'Ubuntu Linux (64-bit)'),
                     self.check('guestOsType', 'linux'),
                     self.check('location', 'eastus'),
                     self.check('nics | [0].virtualNicName', 'Network adapter 1'),
                     self.check('numberOfCores', 1)
                 ])

        # Customizing specific properties of a VM. Changing the
        # size of "Hard disk 1" disk to 21943040 KB,
        # from that specified in the template, and also adding
        # another disk with SCSI controller 0,
        # persistent mode, and 41943040 KB size.
        self.cmd('az vmware vm create -g {rg} -n {name6} \
                 -p {pc} --template {vm_template} -r {rp} \
                 --disk name="Hard disk 1" size=21943040 --disk \
                 name=DiskNameWouldBeReassigned controller=1000 \
                 mode=persistent size=41943040',
                 checks=[
                     self.check('provisioningState', 'Succeeded'),
                     self.check('resourceGroup', '{rg}'),
                     self.check('name', '{name6}'),
                     self.check('amountOfRam', 1024),
                     self.check('disks | [0].virtualDiskName', 'Hard disk 1'),
                     self.check('disks | [0].totalSize', 21943040),
                     self.check('disks | [1].controllerId', '1000'),
                     self.check('disks | [1].independenceMode', 'persistent'),
                     self.check('disks | [1].totalSize', 41943040),
                     self.check('guestOs', 'Ubuntu Linux (64-bit)'),
                     self.check('guestOsType', 'linux'),
                     self.check('location', 'eastus'),
                     self.check('nics | [0].virtualNicName', 'Network adapter 1'),
                     self.check('numberOfCores', 1)
                 ])

        # Deleting the VMs.
        self.cmd('az vmware vm delete -g {rg} -n {name1}')
        self.cmd('az vmware vm delete -g {rg} -n {name2}')
        self.cmd('az vmware vm delete -g {rg} -n {name3}')
        self.cmd('az vmware vm delete -g {rg} -n {name4}')
        self.cmd('az vmware vm delete -g {rg} -n {name5}')
        self.cmd('az vmware vm delete -g {rg} -n {name6}')

    @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    def test_vmware_cs_vm_start_stop(self, resource_group):
        """
        Tests the start/stop APIs for vmware vm.
        """

        self.kwargs.update({
            'name': self.create_random_name(prefix='cli-test', length=24),
            'loc': 'eastus',
            'pc': 'avs-test-eastus',
            'vm_template': 'vm-125',
            'rp': 'resgroup-169',
            'ram': 1024,
            'cores': 1
        })

        # Creating a VM.
        self.cmd('az vmware vm create -g {rg} -n {name} --location {loc} --ram {ram} \
                 --cores {cores}  --private-cloud {pc} --template {vm_template} \
                 --resource-pool {rp}')

        # Testing that VM is in running state
        self.cmd('az vmware vm show -g {rg} -n {name}',
                 checks=[self.check('status', 'running')])

        # Power off the VM
        self.cmd('az vmware vm stop -g {rg} -n {name} --mode poweroff')

        # Testing that VM is in powered off state
        self.cmd('az vmware vm show -g {rg} -n {name}',
                 checks=[self.check('status', 'poweredoff')])

        # Start the VM
        self.cmd('az vmware vm start -g {rg} -n {name}')

        # Testing that VM is in running state
        self.cmd('az vmware vm show -g {rg} -n {name}',
                 checks=[self.check('status', 'running')])

        # Shut down the VM
        self.cmd('az vmware vm stop -g {rg} -n {name} --mode shutdown')

        # Testing that VM is in powered off state
        self.cmd('az vmware vm show -g {rg} -n {name}',
                 checks=[self.check('status', 'poweredoff')])

        # Start the VM
        self.cmd('az vmware vm start -g {rg} -n {name}')

        # Testing that VM is in running state
        self.cmd('az vmware vm show -g {rg} -n {name}',
                 checks=[self.check('status', 'running')])

        # Reboot the VM
        self.cmd('az vmware vm stop -g {rg} -n {name} --mode reboot')

        # Testing that VM is in running state
        self.cmd('az vmware vm show -g {rg} -n {name}',
                 checks=[self.check('status', 'running')])

        # Suspend the VM
        self.cmd('az vmware vm stop -g {rg} -n {name} --mode suspend')

        # Testing that VM is in suspended state
        self.cmd('az vmware vm show -g {rg} -n {name}',
                 checks=[self.check('status', 'suspended')])

        # Deleting the VM.
        self.cmd('az vmware vm delete -g {rg} -n {name}')

    @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    def test_vmware_vm_template_list_and_show(self, resource_group):
        """
        Tests the list and show vm templates command.
        """
        self.kwargs.update({
            'rp': 'resgroup-169',
            'pc': 'avs-test-eastus',
            'vmtemplate': 'vm-125',
            'loc': 'eastus'
        })

        self.cmd('az vmware vm-template list -p {pc} -r {rp} --location {loc}')

        self.cmd('az vmware vm-template show -p {pc} -n {vmtemplate} --location {loc}',
                 checks=[
                     self.check('guestOsType', 'linux'),
                     self.check('guestOs', 'Ubuntu Linux (64-bit)'),
                     self.check('type', 'Microsoft.VMwareCloudSimple/virtualMachineTemplates')
                 ])

    @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    def test_vmware_vnet_list_and_show(self, resource_group):
        """
        Tests the list and show virtual networks command.
        """
        self.kwargs.update({
            'rp': 'resgroup-169',
            'pc': 'avs-test-eastus',
            'vnet': 'dvportgroup-85',
            'loc': 'eastus'
        })

        self.cmd('az vmware virtual-network list -p {pc} -r {rp} --location {loc}')

        self.cmd('az vmware virtual-network show -p {pc} -n {vnet} --location {loc}',
                 checks=[
                     self.check('name', 'Datacenter/Workload01'),
                     self.check('type', 'Microsoft.VMwareCloudSimple/virtualNetworks')
                 ])

    @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    def test_vmware_resource_pool_list_and_show(self, resource_group):
        """
        Tests the list and show resource pools command.
        """
        self.kwargs.update({
            'rp': 'resgroup-169',
            'pc': 'avs-test-eastus',
            'loc': 'eastus'
        })

        self.cmd('az vmware resource-pool list -p {pc} --location {loc}')

        self.cmd('az vmware resource-pool show -p {pc} -n {rp} --location {loc}',
                 checks=[
                     self.check('location', 'eastus'),
                     self.check('name', 'AzCLITest'),
                     self.check('type', 'Microsoft.VMwareCloudSimple/resourcePools')
                 ])

    @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    def test_vmware_private_cloud_list_and_show(self, resource_group):
        """
        Tests the list and show private clouds command.
        """
        self.kwargs.update({
            'pc': 'avs-test-eastus',
            'loc': 'eastus'
        })
        self.cmd('az vmware private-cloud list --location {loc}')

        self.cmd('az vmware private-cloud show -n {pc} --location {loc}',
                 checks=[
                     self.check('location', 'eastus'),
                     self.check('name', '{pc}')
                 ])

    def test_vmware_cs_vm_disk_apis(self):

        self.kwargs.update({
            'name': self.create_random_name(prefix='cli-test', length=24),
            'loc': 'eastus',
            'pc': 'avs-test-eastus',
            'vm_template': 'vm-125',
            'rp': 'resgroup-169',
            'rg': 'az_cli_cs_test'
        })

        # Creating a VM.
        self.cmd('az vmware vm create -g {rg} -n {name} --location {loc} \
                 --private-cloud {pc} --template {vm_template} --resource-pool {rp}')

        # Add a disk with the default values
        self.cmd('az vmware vm disk add -g {rg} --vm-name {name}',
                 checks=[
                     self.check('disks | [1].controllerId', '1000'),
                     self.check('disks | [1].independenceMode', "persistent"),
                     self.check('disks | [1].totalSize', 16777216),
                 ])

        # Add a custom disk
        self.cmd('az vmware vm disk add -g {rg} --vm-name {name} \
                 --mode independent_nonpersistent --size 8388608',
                 checks=[
                     self.check('disks | [2].controllerId', '1000'),
                     self.check('disks | [2].independenceMode', "independent_nonpersistent"),
                     self.check('disks | [2].totalSize', 8388608)
                 ])

        # Show a disk
        self.cmd('az vmware vm disk show -g {rg} --vm-name {name} -n "Hard disk 1"',
                 checks=[
                     self.check('controllerId', '1000'),
                     self.check('independenceMode', "persistent"),
                     self.check('totalSize', 16777216),
                     self.check('virtualDiskName', "Hard disk 1")
                 ])

        # Checking that the number of disk in the VM is 3 now.
        count = len(self.cmd('az vmware vm disk list -g {rg} \
                             --vm-name {name}').get_output_in_json())
        self.assertEqual(count, 3)

        # Delete disks. Among the given disks, two disk are present in VM and one disk is absent.
        # The present disk should be deleted, and an error for the absent disk should be displayed.
        with self.assertRaisesRegexp(CLIError, "Hard disk 4 not present in the given virtual machine."):
            self.cmd('az vmware vm disk delete -g {rg} --vm-name {name} \
                     --disks "Hard disk 1" "Hard disk 2" "Hard disk 4"')

        # Polling till update operation is complete
        vm_status = self.cmd('az vmware vm show -g {rg} -n \
                             {name}').get_output_in_json()["status"]
        while vm_status == "updating":
            vm_status = self.cmd('az vmware vm show -g {rg} -n \
                                 {name}').get_output_in_json()["status"]

        self.cmd('az vmware vm disk add -g {rg} --vm-name {name} \
                 --mode independent_nonpersistent --size 8388608',
                 checks=[
                     self.check('disks | [1].controllerId', '1000'),
                     self.check('disks | [1].independenceMode', "independent_nonpersistent"),
                     self.check('disks | [1].totalSize', 8388608)
                 ])

        # Checking that the number of disk in the VM is 2 now.
        count = len(self.cmd('az vmware vm disk list -g {rg} \
                             --vm-name {name}').get_output_in_json())
        self.assertEqual(count, 2)

        # Deleting the VM.
        self.cmd('az vmware vm delete -g {rg} -n {name}')

    def test_vmware_cs_vm_nic_apis(self):

        self.kwargs.update({
            'name': self.create_random_name(prefix='cli-test', length=24),
            'loc': 'eastus',
            'pc': 'avs-test-eastus',
            'vm_template': 'vm-125',
            'rp': 'resgroup-169',
            'vnet': 'dvportgroup-85',
            'rg': 'az_cli_cs_test'
        })

        # Creating a VM.
        self.cmd('az vmware vm create -g {rg} -n {name} --location {loc} \
                 --private-cloud {pc} --template {vm_template} --resource-pool {rp}')

        # Add a nic with the default values
        self.cmd('az vmware vm nic add -g {rg} --vm-name {name} --virtual-network {vnet}',
                 checks=[
                     self.check('nics | [1].nicType', 'VMXNET3'),
                     self.check('nics | [1].powerOnBoot', None),
                     self.check('nics | [1].network.name', 'Datacenter/Workload01')
                 ])

        # Add a custom nic
        self.cmd('az vmware vm nic add -g {rg} --vm-name {name} \
                 --virtual-network {vnet} --adapter E1000 --power-on-boot false',
                 checks=[
                     self.check('nics | [2].nicType', 'E1000'),
                     self.check('nics | [2].powerOnBoot', None),
                     self.check('nics | [1].network.name', 'Datacenter/Workload01')
                 ])

        # Show a nic
        self.cmd('az vmware vm nic show -g {rg} --vm-name {name} -n "Network adapter 1"',
                 checks=[
                     self.check('nicType', 'VMXNET3'),
                     self.check('powerOnBoot', True),
                     self.check('network.name', 'Datacenter/Workload01'),
                     self.check('virtualNicName', "Network adapter 1")
                 ])

        # Checking that the number of nics in the VM is 3 now.
        count = len(self.cmd('az vmware vm nic list -g {rg} --vm-name {name}').get_output_in_json())
        self.assertEqual(count, 3)

        # Delete nics. Among the given nics, two nics are present in VM and one nic is absent.
        # The present nics should be deleted, and an error for the absent nic should be displayed.
        with self.assertRaisesRegexp(CLIError, 'Network adapter 4 not present in the given virtual machine.'):
            self.cmd('az vmware vm nic delete -g {rg} --vm-name {name} \
                     --nics "Network adapter 1" "Network adapter 2" "Network adapter 4"')

        # Polling till update operation is complete
        vm_status = self.cmd('az vmware vm show -g {rg} -n \
                             {name}').get_output_in_json()["status"]
        while vm_status == "updating":
            vm_status = self.cmd('az vmware vm show -g {rg} -n \
                                 {name}').get_output_in_json()["status"]

        # Add a nic with the default values
        self.cmd('az vmware vm nic add -g {rg} --vm-name {name} --virtual-network {vnet}',
                 checks=[
                     self.check('nics | [1].nicType', 'VMXNET3'),
                     self.check('nics | [1].powerOnBoot', None),
                     self.check('nics | [1].network.name', 'Datacenter/Workload01')
                 ])

        # Checking that the number of nics in the VM is 2 now.
        count = len(self.cmd('az vmware vm nic list -g {rg} --vm-name {name}').get_output_in_json())
        self.assertEqual(count, 2)

        # Deleting the VM.
        self.cmd('az vmware vm delete -g {rg} -n {name}')
