# Azure VMware Solutions by CloudSimple Extension for Azure CLI

This extension provides command to manage Azure VMware Solutions.

## Installing Azure CLI

Please refer to the [install guide](https://docs.microsoft.com/cli/azure/install-azure-cli) for detailed install instructions.

You can also use the extension from Azure Cloud Shell.
[![](https://shell.azure.com/images/launchcloudshell.png "Launch Azure Cloud Shell")](https://shell.azure.com)


## Installing vmware-cs extension

Install by the CLI command:

```
az extension add -n vmware-cs
```

## Quick start

1. Run the `az login` command to log in to your Azure account.

    If the CLI can open your default browser, it will do so and load a sign-in page. Otherwise, you need to open a
    browser page and follow the instructions on the command line to enter an authorization code after navigating to
    [https://aka.ms/devicelogin](https://aka.ms/devicelogin) in your browser. For more information, see the
    [Azure CLI login page](https://docs.microsoft.com/cli/azure/authenticate-azure-cli?view=azure-cli-latest).

2. Use `az account set` with the subscription ID or name you want to switch to.

```
az account set --subscription "My Subscription"
```

3. You can configure defaults such as the resource group and location, or you can also provide these as parameters for each command.

```
az configure --defaults location=MyLocation group=MyResourceGroup
```


## Usage

```
az [group] [subgroup] [command] {parameters}
```

For usage and help content for any command, pass in the -h parameter, for example:

```
az vmware -h

Group
    az vmware : Manage Azure VMware Solution.
        This command group is in preview. It may be changed/removed in a future release.
Subgroups:
    private-cloud   : Manage VMware private clouds.
    resource-pool   : Manage VMware resource pools.
    virtual-network : Manage virtual networks.
    vm              : Manage VMware virtual machines.
    vm-template     : Manage VMware virtual machine templates.
```

You can views the various commands and its usage in [Microsoft docs](https://docs.microsoft.com/en-us/cli/azure/ext/vmware-cs/?view=azure-cli-latest)

This extension provides CLI commands to:
1. Create, list, show, update, delete, start, stop - VMware Virtual Machines by CloudSimple. You can update disks, nics, and the tags of a VM. More update capabilities would be supported in future releases.
    For creating a VMware VM by CloudSimple, a CloudSimple private cloud should be provisioned, which involves creating a CloudSimple service and provisioning a minimum of 3 nodes.
2. List and show - private clouds, resource pools, virtual machine templates, and virtual networks.

## Removing extension

Extension can be removed using the following CLI command:

```
az extension remove -n vmware-cs
```


## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
