#!/bin/bash

# Community Script to generate some behaiviours in Azure - and then polygraph data in Lacework
# This script is provided as a community resource for use with Lacework products
# It is provided as is, with no warranty or support
# It is your responsibility to test and validate the script before running in any capacity
# It is your responsibility to ensure the script does not violate any policies or regulations within your organisation


# What does it do?
# This script will create a user, app and storage account, then upload a file to the storage account
# It will then delete the user, app and storage account
# It will then create a log file in the current directory with the name azureevilscriptnnnnnnn.log

# It can be run on a local machine with the Azure CLI installed, or in Azure Cloud Shell

# Replace these values with your own
region="australiaeast" # Region to deploy the scripts resources into
subscription_id="8f3fooooooooooooa13d8" # subscription id
yourtenant="fooooooooooo" # the bit before the .onmicrosoft.com


#################### Editing below here can cause problems... ####################

# NOTE:
# Leave these alone, unless you really want to tune it
password=$(openssl rand -base64 15)
random=$((RND=RANDOM<<8|RANDOM))
app_name="evilapp$random"
resource_group="evilgroup$random"
storage_account="evilstorage$random"
user_principal_name="eviluser$random"

red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

# NOTE:
# Start of script
{


echo  ${grn}Here we go...${end}
echo  ${blu}Random resource groupname..... $resource_group${end}
echo  ${grn}There are sleeps in this script to spread out the activity and allow Azure${end}
echo  ${grn}resources to be ready${end}

# Login as genuine privileged user
echo  ${mag}Login as base / root user that can create accounts etc, check prompt below${end}
az account show --query user --output tsv
az login 
echo  ${mag}Now logged in as....${end}
az account show --query user --output tsv


# Create Resource Group
echo  ${cyn}Create user, app and storage${end}
echo  ${cyn}Create RG $resource_group${end}
az group create --name "$resource_group" --location "$region"

echo  ${cyn}Sleeping 20 for Azure to catchup${end}
sleep 20

# Create Storage Account
echo  ${cyn}Create Storage Account $storage_account${end}
az storage account create --name "$storage_account" --resource-group "$resource_group" --location "$location" --sku Standard_LRS

# Create a User
echo  ${cyn}Create user - Evil User - $user_principal_name@$yourtenant.onmicrosoft.com${end}
az ad user create --display-name "evil user$random" --user-principal-name "$user_principal_name@$yourtenant.onmicrosoft.com" --password "$password"

echo  ${cyn}Sleeping 20 for Azure to catchup${end}
sleep 20

# Create a Service Principal
echo  ${cyn}Create a Service Principal${end}
sp_info=$(az ad sp create-for-rbac --name "$app_name" --role contributor --scopes "/subscriptions/$subscription_id")

# Extract relevant information
app_id=$(echo $sp_info | jq -r .appId)
app_secret=$(echo $sp_info | jq -r .password)

# Assign Permissions to the User
echo  ${cyn}Get user_object_id${end}
user_object_id=$(az ad user show --id "$user_principal_name@$yourtenant.onmicrosoft.com" --query id --output tsv)
echo  ${cyn}It is $user_object_id${end}

echo  ${cyn}Sleeping 20 for Azure to catchup${end}
sleep 20

echo  ${cyn}Assign Storage Blob Data Contributor role to make polygraph${end}
# Assign Storage Blob Data Contributor role to the service principal
az role assignment create --assignee $user_object_id --role "Storage Blob Data Contributor" --scope "/subscriptions/$subscription_id/resourceGroups/$resource_group/providers/Microsoft.Storage/storageAccounts/$storage_account"

echo  ${cyn}Sleeping 20 for Azure to catchup${end}
sleep 20

echo  ${cyn}Assign Contributor role to the user $user_object_id${end}
# Assign Contributor role to the user directly
az role assignment create --assignee-object-id $user_object_id --role "contributor" --scope "/subscriptions/$subscription_id"

# Print Service Principal (App) ID and Secret
echo  ${cyn}App Info $app_id $app_secret${end}
echo "Service Principal (App) ID: $app_id"
echo "Service Principal (App) Secret: $app_secret"

echo  ${cyn}Who are you?${end}
az ad signed-in-user show --query userPrincipalName -o tsv

## Do funky things

## Change to new user
echo  ${red}Changing to new evil user $user_principal_name@$yourtenant.onmicrosoft.com ...${end}
echo  ${cyn}Who are you?${end}
az account show --query user --output tsv
az login --username $user_principal_name@$yourtenant.onmicrosoft.com --password $password
echo  ${cyn}Who are you now, evil of course.....?${end}
az account show --query user --output tsv

echo  ${red}Do funky things....${end}
echo  ${cyn}Do some Recon....${end}

echo  ${yel}List VMs${end}
az vm list
echo  ${yel}List VMs names${end}
az vm list --query "[].[name]" -o table
echo  ${yel}List Web Apps${end}
az webapp list
echo  ${yel}List functionapp${end}
az functionapp list --query "[].[name]" -o table
echo  ${yel}List storage${end}
az storage account list
echo  ${yel}List Keyvaults${end}
az keyvault list

echo  ${yel}Get file and upload${end}
curl -H "Accept: application/json" https://icanhazdadjoke.com/ > evilfile.json
echo  ${cyn}Enjoy the dad joke.....${end}
cat evilfile.json
#echo https://$storage_account.blob.core.windows.net/

echo  ${cyn}Sleeping 20 for Azure to catchup${end}
sleep 20

az storage container create --account-name $storage_account --name mycontainer --auth-mode login

echo  ${cyn}Uplodaing file.....${end}
az storage blob upload \
    --account-name $storage_account \
    --container-name mycontainer \
    --name evilfile.json \
    --file evilfile.json \
    --auth-mode login

echo  ${cyn}Here are the files we uploaded${end}
az storage blob list --account-name $storage_account --container-name mycontainer --output table
echo  ${cyn}Ha, ha, ha arnt we evil....${end}


echo  ${cyn}Sleeping 60 for manual Azure portal checks before auto delete${end}
sleep 60

###############
## Cleanup
echo  ${cyn}Deleting created resources - log back in as real user${end}
echo  ${mag}Login as base / root user that can delete accounts etc${end}
az account show --query user --output tsv
az login 
echo  ${mag}Now logged in as....${end}
az account show --query user --output tsv

# Delete the User
az ad user delete --id "$user_object_id"

# Delete the Service Principal (App)
az ad app delete --id "$app_id"

# Delete the Resource Group
az group delete --name "$resource_group" --yes --no-wait

echo ${red}"User $user_object_id@$yourtenant.onmicrosoft.com, Service Principal (App), and Resource Group '$resource_group' deleted."${end}

} | tee azureevilscript$random.log

echo  ${grn}Script complete, check log file azureevilscript$random.log${end}



