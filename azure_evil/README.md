# Azure Evil Script

Script to generate traffic into azure to look a little bit "evil"

## What does it do?
* This script will create a user, app and storage account, then upload a file to the storage account
* It will then delete the user, app and storage account
* It will then create a log file in the current directory with the name azureevilscriptnnnnnnn.log

```bash
git clone 

chmod +x baduser_azure_activity.sh
```

While running the script you will be asked to login to Azure, the first user should be capable of carrying out the tasks in the script, create a user, app etc.

Once logged in the script will carry out the functions and switch to 

```bash
./baduser_azure_activity.sh
```

![Example Alert](/Azure%20Evil/images/Example_Alert.png)

![Example Polygraph](/Azure%20Evil/images/Example_polygraph.png)