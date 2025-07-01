# Create Azure Machine Learning Studio Workspace
To use Azure Machine Learning, you'll first need a workspace. The workspace is the central place to view and manage all the artifacts and resources you create.

Other ways to create a workspace are via the [Azure portal or SDK](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace), [the CLI](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace-cli), [Azure PowerShell](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace-powershell), or the [Visual Studio Code extension](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-setup-vs-code).

## Create the workspace
The workspace is the top-level resource for your machine learning activities, providing a centralized place to view and manage the artifacts you create when you use Azure Machine Learning.

If you already have a workspace, skip this section and continue to [Create a compute instance](/part-1/1-create-ml-compute-instance.md).

If you don't yet have a workspace, create one now:
1. Sign in to Azure Machine Learning studio  
2. Select Create workspace  
3. Provide the following information to configure your new workspace:  

| Field           | Description |
|-----------------|-------------|
| Workspace name  | Enter a unique name that identifies your workspace. Names must be unique across the resource group. Use a name that's easy to recall and to differentiate from workspaces created by others. The workspace name is case-insensitive. |
| Friendly name   | This name is not restricted by Azure naming rules. You can use spaces and special characters in this name. |
| Hub             | A hub allows you to group related workspaces together and share resources. If you have access to a hub, select it here. If you don't have access to a hub, leave this blank. |

4. If you did not select a hub, provide the advanced information. If you selected a hub, these values are taken from the hub.

| Field          | Description |
|----------------|-------------|
| Subscription   | Select the Azure subscription that you want to use. |
| Resource group | Use an existing resource group in your subscription or enter a name to create a new resource group. A resource group holds related resources for an Azure solution. You need contributor or owner role to use an existing resource group. For more information about access, see Manage access to an Azure Machine Learning workspace. |
| Region         | Select the Azure region closest to your users and the data resources to create your workspace. |  

5. Select Create to create the workspace

