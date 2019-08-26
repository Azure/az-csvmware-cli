# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import unittest

from azure_devtools.scenario_tests import AllowLargeResponse
from azure.cli.testsdk import (ScenarioTest, ResourceGroupPreparer)
from msrestazure.azure_exceptions import CloudError
from knack.util import CLIError
import logging

TEST_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))


class Vmware_csScenarioTest(ScenarioTest):
    """
    Test for AVS by CloudSimple CLI commands.
    """

    @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    def test_vmware_cs_provider(self, resource_group):
        """
        Tests the set-provider and get-provider commands.
        """
        self.kwargs.update({
            'dummy_name': self.create_random_name(prefix='cli-test', length=24),
            'provider_name': 'cs',
            'CURRENT_PROVIDER_FIELD_NAME': 'current_provider'
        })

        # Set the provider to CloudSimple (cs).
        self.cmd('az vmware set-provider -n {provider_name}')

        # Check that the provider is cs
        self.cmd('az vmware get-provider',
                 checks=[self.check('{CURRENT_PROVIDER_FIELD_NAME}', '{provider_name}')])

        # Check that setting any dummy provider will result in an error
        with self.assertRaises(SystemExit):
            self.cmd('az vmware set-provider -n {dummy_name}')

        # Check that the provider is still cs
        self.cmd('az vmware get-provider',
                 checks=[self.check('{CURRENT_PROVIDER_FIELD_NAME}', '{provider_name}')])

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
            'rp': 'resgroup-52',
            'ram': 1024,
            'cores': 1
        })

        # Ensuring that CloudSimple commands are available by setting the correct provider.
        self.cmd('az vmware set-provider -n cs')

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
            'name': self.create_random_name(prefix='cli-test', length=24),
            'loc': 'eastus',
            'pc': 'avs-test-eastus',
            'vm_template': 'vm-125',
            'rp': 'resgroup-52',
            'ram': 1024,
            'cores': 1
        })

        # Ensuring that CloudSimple commands are available by setting the correct provider.
        self.cmd('az vmware set-provider -n cs')

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

        # Testing update command
        self.cmd('az vmware vm update -g {rg} -n {name} --set tags.foo=boo', checks=[
            self.check('tags.foo', 'boo')
        ])

        # Deleting a VM.
        self.cmd('az vmware vm delete -g {rg} -n {name}')

        # Checking that the number of VM in our rg is 0 now.
        count = len(self.cmd('az vmware vm list -g {rg}').get_output_in_json())
        self.assertEqual(count, 0)

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
            'rp': 'resgroup-52',
            'ram': 1024,
            'cores': 1
        })

        # Ensuring that CloudSimple commands are available by setting the correct provider.
        self.cmd('az vmware set-provider -n cs')

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

    @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    def test_vmware_list_vm_template(self, resource_group):
        """
        Tests the list vm templates command.
        """
        self.kwargs.update({
            'rp': 'resgroup-52',
            'pc': 'avs-test-eastus',
            'vmtemplate': 'vm-125'
        })

        self.cmd('az vmware vm-template list -pc {pc} -rp {rp}')

        self.cmd('az vmware vm-template list -pc {pc} -n {vmtemplate}',
                 checks=[
                     self.check('guestOsType', 'linux'),
                     self.check('guestOs', 'Ubuntu Linux (64-bit)'),
                     self.check('type', 'Microsoft.VMwareCloudSimple/virtualMachineTemplates')
                 ])

    @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    def test_vmware_list_vnet(self, resource_group):
        """
        Tests the list virtual networks command.
        """
        self.kwargs.update({
            'rp': 'resgroup-52',
            'pc': 'avs-test-eastus',
            'vnet': 'dvportgroup-85'
        })

        self.cmd('az vmware virtual-network list -pc {pc} -rp {rp}')

        self.cmd('az vmware virtual-network list -pc {pc} -n {vnet}',
                 checks=[
                     self.check('name', 'Datacenter/Workload01'),
                     self.check('type', 'Microsoft.VMwareCloudSimple/virtualNetworks')
                 ])

    @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    def test_vmware_list_resource_pool(self, resource_group):
        """
        Tests the list resource pools command.
        """
        self.kwargs.update({
            'rp': 'resgroup-52',
            'pc': 'avs-test-eastus'
        })

        self.cmd('az vmware resource-pool list -pc {pc}')

        self.cmd('az vmware resource-pool list -pc {pc} -n {rp}',
                 checks=[
                     self.check('location', 'eastus'),
                     self.check('name', 'Workload'),
                     self.check('type', 'Microsoft.VMwareCloudSimple/resourcePools')
                 ])

    @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    def test_vmware_cs_region(self, resource_group):
        """
        Tests the set-region and get-region commands.
        """
        self.kwargs.update({
            'region_id': 'eastus',
            'CONFIG_REGION_FIELD_NAME': 'region_id'
        })

        # Set the region to eastus.
        self.cmd('az vmware set-region -n {region_id}')

        # Check that the region is eastus
        self.cmd('az vmware get-region',
                 checks=[self.check('{CONFIG_REGION_FIELD_NAME}', '{region_id}')])

    @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    def test_vmware_list_private_cloud(self, resource_group):
        """
        Tests the list private clouds command.
        """

        self.cmd('az vmware private-cloud list')

    # @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    # def test_vmware_cs_vm_add_disk(self, resource_group):

    #     self.kwargs.update({
    #         'name': self.create_random_name(prefix='cli-test', length=24),
    #         'loc': 'eastus',
    #         'pc': 'avs-test-eastus'
    #     })

    #     # Ensuring that CloudSimple commands are available by setting the correct provider.
    #     self.cmd('az vmware set-provider -n cs')

    #     # Creating a VM.
    #     self.cmd('az vmware vm create -g {rg} -n {name} --location {loc} --ram 1024 --cores 1 \
    #              --private-cloud {pc} --template vm-125 --resource-pool resgroup-52')

    #     # Add a disk
    #     self.cmd('az vmware vm add-disk -g {rg} -n {name}')

    # @ResourceGroupPreparer(name_prefix='cli_test_vmware_cs', parameter_name_for_location='eastus')
    # def test_vmware_cs_vm_add_nic(self, resource_group):

    #     self.kwargs.update({
    #         'name': self.create_random_name(prefix='cli-test', length=24),
    #         'loc': 'eastus',
    #         'pc': 'avs-test-eastus'
    #     })

    #     # Ensuring that CloudSimple commands are available by setting the correct provider.
    #     self.cmd('az vmware set-provider -n cs')

    #     # Creating a VM.
    #     self.cmd('az vmware vm create -g {rg} -n {name} --location {loc} --ram 1024 --cores 1 \
    #              --private-cloud {pc} --template vm-125 --resource-pool resgroup-52')

    #     # Add a disk
    #     self.cmd('az vmware vm add-disk -g {rg} -n {name} --virtual-network dvportgroup-85')
