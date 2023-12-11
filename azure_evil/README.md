# Azure Evil Script

Script to generate Azure api traffic to look a little bit "evil"

It can be run on a local machine with the Azure CLI installed, or in Azure Cloud Shell

## What does it do?
* This script will create a user, app and storage account, then upload a file to the storage account
* It will then delete the user, app and storage account
* It will then create a log file in the current directory with the name `azureevilscriptnnnnnnn.log`

### Clone the repo and make the file executable
```bash
git clone https://github.com/J-C-B/lwpublic.git 

cd lwpublic
cd azure_evil

chmod +x baduser_azure_activity.sh
```
### Edit the script with your subscription id etc

```bash
# Replace these values with your own
region="australiaeast" # Region to deploy the scripts resources into
subscription_id="8f3fooooooooooooa13d8" # subscription id
yourtenant="fooooooooooo" # the bit before the .onmicrosoft.com
```

### Run the script

While running the script you will be asked to login to Azure, the first user should be capable of carrying out the tasks in the script, create a user, app etc.

Once logged in the script will carry out the functions and switch to its newly created "evil" user, perform some recon and then upload an "evil" file to the "evil" storage.

Run the script by executing

```bash
./baduser_azure_activity.sh
```
## Example Polygraph showing activity in the Azure Activity Dossier
![Example Polygraph](/azure_evil/images/Example_polygraph.png)

## Example Alert from the script
![Example Alert](/azure_evil/images/Example_Alert.png)

## Example Azure Resource
![Example Resource](/azure_evil/images/Azure_Resource.png)

## Example Azure User
![Example Azure User](/azure_evil/images/Azure_User.png)